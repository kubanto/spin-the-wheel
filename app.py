from flask import Flask, request, jsonify, send_from_directory
import sqlite3, os
from datetime import datetime

DB_PATH = "/data/scores.db"
app = Flask(__name__, static_folder="static")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
      CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player TEXT,
        total_score INTEGER,
        played_at TEXT
      )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/score", methods=["POST"])
def save_score():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO scores (player, total_score, played_at) VALUES (?, ?, ?)",
        (data["player"], data["total"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.route("/scores")
def get_scores():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute(
        "SELECT player, total_score, played_at FROM scores ORDER BY total_score DESC"
    ).fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    os.makedirs("/data", exist_ok=True)
    init_db()
    app.run(host="0.0.0.0", port=5000)
