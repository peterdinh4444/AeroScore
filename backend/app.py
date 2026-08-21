import os 
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__) # reserves port on your ip
DATABASE_URL = os.environ.get("DATABASE_URL")
ADMIN_KEY = os.environ.get("ADMIN_KEY")

# Limiter object 
limiter = Limiter(get_remote_address, app=app, default_limits=[])

MAX_NAME_LENGTH = 10
MAX_SCORE = 1000



# replaced sqlite3 connection 
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


def validate_score_submission(data):
    # edge case check
    if not data or "player_name" not in data or "player_score" not in data:
        return False, "player data is missing"

    name = data["player_name"]
    score = data["player_score"]

    # NAME CHECK
    if not isinstance(name, str):
        return False, "player_name must be a string"
    name = name.strip()
    if len(name)>MAX_NAME_LENGTH:
        return False, f"player_name must be {MAX_NAME_LENGTH} characters or less"
    if not name.isalnum():
        return False, "player_name must be alphanumeric"


    # SCORE CHECK
    if isinstance(score, bool) or not isinstance(score, int):
        return False, "player_score must be an integer"
    if score>MAX_SCORE: 
        return False, "player_score is too large"
    if score<0:
        return False, "player_score cannot be negative"


    return True, "player data submission is valid"

# run method when POST request arrives at address
@app.route("/api/score", methods=["POST"])
@limiter.limit("6 per minute")
def submit_score():
    # get data using request methods
    data = request.get_json()

    is_valid, error = validate_score_submission(data)

    # safe gaurd for bad data, return client side error
    if not is_valid:
        return jsonify({"error": error}), 400

    # database insertion
    player_name = data["player_name"].strip()
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
@limiter.limit("30 per minute")
def get_leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT player_name, player_score, created_at FROM leaderboard ORDER BY player_score DESC LIMIT 10") 
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows), 200

@app.route("/api/admin/clear-leaderboard", methods=["DELETE"])
def clear_leaderboard():
    input_key = request.headers.get("X-Admin-Secret")
    if not input_key or input_key != ADMIN_KEY:
        return jsonify({"error": "Invalid or missing admin key"}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE leaderboard")
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Leaderboard successfully deleted"})



    
if __name__ == "__main__":
    app.run()