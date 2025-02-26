from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import random
import string

app = Flask(__name__)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()
    
    # Table for storing unique voter codes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            used INTEGER DEFAULT 0
        )
    """)

    # Table for voting sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voting_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            candidates TEXT NOT NULL,
            active INTEGER DEFAULT 0
        )
    """)

    # Table for storing votes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            candidate TEXT NOT NULL,
            voter_code TEXT NOT NULL UNIQUE,
            FOREIGN KEY (session_id) REFERENCES voting_sessions(id)
        )
    """)

    conn.commit()
    conn.close()


init_db()



def get_db_connection():
    conn = sqlite3.connect("voting.db", timeout=10)  # Increase timeout to avoid conflicts
    conn.row_factory = sqlite3.Row
    return conn

def enable_wal_mode():
    conn = sqlite3.connect("voting.db")
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.close()



# ✅ Generate a Unique 6-Digit Code
def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route("/", methods=["GET", "POST"])
def index_route():
    if request.method == "POST":
        voter_code = request.form["code"].strip().upper()

        conn = sqlite3.connect("voting.db")
        cursor = conn.cursor()

        # Check if the code exists and has not been used
        cursor.execute("SELECT * FROM codes WHERE code = ? AND used = 0", (voter_code,))
        code_entry = cursor.fetchone()

        conn.close()

        if code_entry:
            return redirect(f"/cast_vote?code={voter_code}")  # Redirect to voting page with voter code
        else:
            return render_template("index.html", error="Invalid or already used code.")

    return render_template("index.html", error=None)


# ✅ Route: Admin Panel
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

# ✅ Route: Generate & Store a Code
@app.route('/generate_code', methods=['POST'])
def generate_code():
    code = generate_unique_code()
    try:
        conn = sqlite3.connect("voting.db", timeout=10)  # Increase timeout to avoid conflicts
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        print(f"Inserting code: {code}")  # Debug message
        cursor.execute("INSERT INTO codes (code, used) VALUES (?, ?)", (code, 0))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "code": code})
    except Exception as e:
        print(f"Error: {e}")  # Debug error message
        return jsonify({"success": False, "error": str(e)})


@app.route("/start_voting", methods=["POST"])
def start_voting():
    data = request.json
    session_name = data["session_name"]
    candidates = ",".join(data["candidates"])

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()
    
    # Deactivate any active session before starting a new one
    cursor.execute("UPDATE voting_sessions SET active = 0")
    cursor.execute("INSERT INTO voting_sessions (name, candidates, active) VALUES (?, ?, 1)", (session_name, candidates))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/stop_voting", methods=["POST"])
def stop_voting():
    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE voting_sessions SET active = 0")
    conn.commit()
    conn.close()
    
    return jsonify({"success": True})

@app.route("/check_voting_status")
def check_voting_status():
    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, candidates FROM voting_sessions WHERE active = 1 LIMIT 1")
    session = cursor.fetchone()
    conn.close()

    if session:
        return jsonify({"active": True, "candidates": session[1].split(",")})
    return jsonify({"active": False})

@app.route("/cast_vote")
def cast_vote():
    voter_code = request.args.get("code")  # Get voter code from URL

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    # Get active voting session
    cursor.execute("SELECT id, name, candidates FROM voting_sessions WHERE active = 1 LIMIT 1")
    session = cursor.fetchone()

    conn.close()

    if session:
        session_id, session_name, candidates = session
        candidates_list = candidates.split(",")

        return render_template("voter.html", session_id=session_id, session_name=session_name, candidates=candidates_list, voter_code=voter_code)
    else:
        return "No active voting session.", 400

@app.route("/vote", methods=["POST"])
def vote():
    data = request.json
    print("Received Data:", data)

    voter_code = data['code']
    candidate = data['candidate']

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    # Get the current active session
    cursor.execute("SELECT id FROM voting_sessions WHERE active = 1 LIMIT 1")
    session = cursor.fetchone()

    if not session:
        conn.close()
        return jsonify({"success": False, "error": "No active voting session."}), 400

    session_id = session[0]

    # Check if this voter code has already voted in this session
    cursor.execute("SELECT COUNT(*) FROM votes WHERE session_id = ? AND voter_code = ?", (session_id, voter_code))
    already_voted = cursor.fetchone()[0]

    if already_voted > 0:
        conn.close()
        return jsonify({"success": False, "error": "You have already voted in this session."}), 400

    # Store the vote with voter_code
    cursor.execute("INSERT INTO votes (session_id, candidate, voter_code) VALUES (?, ?, ?)", (session_id, candidate, voter_code))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Vote cast successfully!"})

@app.route("/get_vote_analysis", methods=["GET"])
def get_vote_analysis():
    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    # Count total votes
    cursor.execute("SELECT COUNT(*) FROM votes")
    total_votes = cursor.fetchone()[0]

    # Count votes per candidate
    cursor.execute("SELECT candidate, COUNT(*) FROM votes GROUP BY candidate")
    votes_per_candidate = cursor.fetchall()

    candidate_votes = {candidate: {"votes": count} for candidate, count in votes_per_candidate}

    conn.close()

    return jsonify({
        "success": True,
        "total_votes": total_votes,
        "candidate_votes": candidate_votes
    })
@app.route('/clear_db', methods=['POST'])
def clear_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM votes")  # Clears the "votes" table
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "All votes have been cleared!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
