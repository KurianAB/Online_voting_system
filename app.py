from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import random
import string

app = Flask(__name__)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voting_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            candidates TEXT NOT NULL,
            active INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            candidate TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES voting_sessions(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()


# Database Connection
def get_db_connection():
    conn = sqlite3.connect('voting_system.db')
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Generate a Unique 6-Digit Code
def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/', methods = ["GET" , "POST"])
def index_route():
    return render_template('index.html')

# ✅ Route: Admin Panel
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

# ✅ Route: Generate & Store a Code
@app.route('/generate_code', methods=['POST'])
def generate_code():
    code = generate_unique_code()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO codes (code, used) VALUES (?, ?)", (code, 0))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "code": code})

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

@app.route("/vote", methods=["POST" ])
def vote():
    if request.method == "POST":
        data = request.json
        candidate = data["candidate"]

        conn = sqlite3.connect("voting.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO votes (session_id, candidate) VALUES ((SELECT id FROM voting_sessions WHERE active = 1), ?)", (candidate,))
        conn.commit()
        conn.close()

        return jsonify({"success": True})

# Route: Clear Database
@app.route('/clear_db', methods=['POST'])
def clear_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM codes")
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Database cleared!"})


if __name__ == '__main__':
    app.run(debug=True)
