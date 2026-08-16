import os 
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__) # reserves port on your ip
DATABASE_URL = os.environ.get("DATABASE_URL")



def get_db_connection():
    if not DATABASE_URL: raise ValueError("DATABASE_URL variable missing")

    db_url = DATABASE_URL
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(db_url)




def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # initializes database with table of name, score, and timestamps 
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS leaderboard (
            id SERIAL PRIMARY KEY,
            player_name TEXT NOT NULL,
            player_score INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# db gets initialized on any platform 
init_db()


# run method when POST request arrives at address
@app.route("/api/score", methods=["POST"])
def submit_score():
    # get data using request methods
    data = request.get_json()

    # safe gaurd for bad data, return client side error
    if not data or "player_name" not in data or "player_score" not in data:
        return jsonify({"error": "player data is missing"}), 400

    # database insertion
    player_name = data["player_name"]
    player_score = data["player_score"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (player_name, player_score) VALUES (%s, %s)",
                    (player_name, player_score))
    conn.commit()
    cursor.close()
    conn.close()

    # code 2XX for success!
    return jsonify({"message": "Score was succesfully submitted"}), 201

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT player_name, player_score, created_at FROM leaderboard ORDER BY player_score DESC LIMIT 10") 
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows), 200

if __name__ == "__main__":
    app.run()