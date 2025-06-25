#Commit.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = 'commits.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS commits (
                path TEXT,
                hash_code TEXT PRIMARY KEY,
                message TEXT,
                timestamp TEXT
            )
        ''')

@app.route('/commits', methods=['POST'])
def add_commit():
    data = request.json
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute(
                'INSERT INTO commits (path, hash_code, message, timestamp) VALUES (?, ?, ?, ?)',
                (data['path'], data['hash_code'], data['message'], data['timestamp'])
            )
            return '', 200
        except sqlite3.IntegrityError:
            return 'Commit already exists', 400

@app.route('/commits/row', methods=['GET'])
def get_commit():
    path = request.args.get('path')
    hash_code = request.args.get('hash_code')
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            'SELECT path, hash_code, message, timestamp FROM commits WHERE path=? AND hash_code=?',
            (path, hash_code)
        )
        row = cur.fetchone()
        if row:
            return jsonify(row={
                "path": row[0],
                "hash_code": row[1],
                "message": row[2],
                "timestamp": row[3]
            })
        return jsonify(row=None)

@app.route('/commits/all', methods=['GET'])
def get_all_commits():
    path = request.args.get('path')
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            'SELECT path, hash_code, message, timestamp FROM commits WHERE path=?',
            (path,)
        )
        rows = [
            {"path": r[0], "hash_code": r[1], "message": r[2], "timestamp": r[3]}
            for r in cur.fetchall()
        ]
        return jsonify(rows=rows)

@app.route('/commits/is_empty', methods=['GET'])
def is_empty():
    path = request.args.get('path')
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            'SELECT COUNT(*) FROM commits WHERE path=?',
            (path,)
        )
        count = cur.fetchone()[0]
        return jsonify(is_empty=(count == 0))

@app.route('/commits/last', methods=['GET'])
def get_last_commit():
    path = request.args.get('path')
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            'SELECT hash_code FROM commits WHERE path=? ORDER BY timestamp DESC LIMIT 1',
            (path,)
        )
        row = cur.fetchone()
        return jsonify(hash_code=row[0] if row else None)

if __name__ == '__main__':
    init_db()
    app.run(port=8000)