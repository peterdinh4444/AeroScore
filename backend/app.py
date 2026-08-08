import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "leaderboard.db"



def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # initializes database with table of name, score, and timestamps 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

@app.route()
def submit_score():
    pass

def get_leaderboard():
    pass 

if __name__ == "__main__":
    pass
    #app.run(debug = True)