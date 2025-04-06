    

# Online Code-Based Voting System

A lightweight, secure, and user-friendly online voting platform built using Flask and SQLite. This system enables administrators to create voting sessions, generate unique voter codes, and analyze results with ease. Voters can securely log in using a 6-digit alphanumeric code to cast their vote.


## Features

- **Unique Code-Based Voter Login**
- **Admin Dashboard** with:
  - Generate unique 6-digit codes for voters
  - Create and manage Voting sessions
  - Real-time session control (start/stop)
  - Post-session analysis
- **Voting Mode**:
  - Vote for one among multiple candidates
  - Automatic winner calculation
- **Analysis Storage** for all past sessions
- **Built using:** Flask, SQLite, HTML, CSS, and JavaScript



## Deployment

To run the project locally:

1. Clone the Repository

```bash
git clone https://github.com/KurianAB/Online_voting_system.git
cd Online_voting_system
```
2. Set Up Virtual Environment (Recommended)

```bash
venv\Scripts\activate.bat
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run the Application
```bash
python app.py
```



## Usage

- **Admin Panel**
  - Navigate to */rgaheruikgbyaeurygabo* (Admin Panel)
  - Generate codes, start/stop sessions, and view session-wise analysis
- **Voter Panel**:
  - Voter enters their unique 6-digit alphanumeric code on the homepage (/)
  - If a session is active, Voter selects a candidate and submits their vote
  - After submission, a confirmation message is shown


## Screenshots
**Admin Panel**

![Generate Unique Code](https://github.com/KurianAB/Online_voting_system/blob/main/Screenshots/Screenshot231500.png)

![Start a Voting Session](https://github.com/KurianAB/Online_voting_system/blob/main/Screenshot231510.png)

![Fetch Analysis](https://github.com/KurianAB/Online_voting_system/blob/main/Screenshots/Screenshot231447.png)

![Clear DB](https://github.com/KurianAB/Online_voting_system/blob/main/Screenshots/Screenshot231710.png)

**User**

![UserView](https://github.com/KurianAB/Online_voting_system/blob/main/Screenshots/UserView.png)

## Use Cases

**1. Student Council Elections**
  
 - Schools, colleges, or universities can use this to conduct student representative elections securely.

 - Unique codes ensure one vote per student without needing personal logins.

**2. Event-Based Audience Polling**
  - During live events, hackathons, talent shows, or debates, organizers can give attendees a code to vote for their favorite participants.

  - Quick and anonymous participation with real-time results.

**3. Internal Team or Organization Voting**
  - Perfect for small teams or companies wanting to vote on decisions (e.g., best project idea, team awards).

  - No login hassles—just distribute codes internally.

**4. Clubs or Community Groups**
  - Clubs (book clubs, hobby clubs, local communities) can vote on plans or leadership in a simple way.

  - Easy to run and manage even with non-technical participants.

**5. Remote Voting Scenarios**
  - Ideal for situations where voters are distributed remotely but a central admin manages the process.

  - Voters only need access to a browser and a valid code.

**6. Hackathons & Competitions**
  - Let participants vote on the best ideas or demos using assigned codes, preventing spam or multiple votes.
## Support

For support, email kurianabraham701@gmail.com



