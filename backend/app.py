import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__) # reserves port on your ip
DB_NAME = "leaderboard.db"



def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # initializes database with table of name, score, and timestamps 
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            player_score INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# run method when POST request arrives at address
@app.route("/api/score", methods=["POST"])
def submit_score():
    # get data using request methods
    data = request.get_json()

    # safe gaurd for bad data, return client side error
    if not data or "player_name" not in data or "player_score" not in data:
        return jsonify({"error: player data is missing"}), 400

    # database insertion
    player_name = data["player_name"]
    player_score = data["player_score"]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (player_name, player_score) VALUES (?, ?)",
                    (player_name, player_score))
    conn.commit()
    conn.close()

    # code 2XX for success!
    return jsonify({"message: Score was succesfully submitted"}), 201

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row #runs before cursor so cursor inherits formating 
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, player_score, created_at FROM leaderboard ORDER BY player_score DESC LIMIT 10") 
    rows = cursor.fetchall()
    conn.close()

    leaderboard = [dict(row) for row in rows]

    return jsonify(leaderboard), 200

if __name__ == "__main__":
    pass
    init_db()
    app.run(debug = True)