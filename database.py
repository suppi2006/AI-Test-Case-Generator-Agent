
import sqlite3
import json
from datetime import datetime

DATABASE_NAME = "test_cases.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS test_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement TEXT NOT NULL,
            feature TEXT,
            testing_purpose TEXT,
            assumptions TEXT,
            test_cases TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_test_cases(requirement, result):
    conn = get_connection()

    conn.execute("""
        INSERT INTO test_history (
            requirement,
            feature,
            testing_purpose,
            assumptions,
            test_cases,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        requirement,
        result.get("feature", ""),
        result.get("testing_purpose", ""),
        json.dumps(result.get("assumptions", [])),
        json.dumps(result.get("test_cases", [])),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_history():
    conn = get_connection()

    rows = conn.execute("""
        SELECT * FROM test_history
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    history = []

    for row in rows:
        item = dict(row)
        item["assumptions"] = json.loads(item["assumptions"])
        item["test_cases"] = json.loads(item["test_cases"])
        history.append(item)

    return history


def get_history_by_id(history_id):
    conn = get_connection()

    row = conn.execute("""
        SELECT * FROM test_history
        WHERE id = ?
    """, (history_id,)).fetchone()

    conn.close()

    if row is None:
        return None

    item = dict(row)
    item["assumptions"] = json.loads(item["assumptions"])
    item["test_cases"] = json.loads(item["test_cases"])

    return item


def update_history(history_id, result):
    conn = get_connection()

    conn.execute("""
        UPDATE test_history
        SET feature = ?,
            testing_purpose = ?,
            assumptions = ?,
            test_cases = ?
        WHERE id = ?
    """, (
        result.get("feature", ""),
        result.get("testing_purpose", ""),
        json.dumps(result.get("assumptions", [])),
        json.dumps(result.get("test_cases", [])),
        history_id
    ))

    conn.commit()
    conn.close()


def delete_history(history_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM test_history
        WHERE id = ?
    """, (history_id,))

    conn.commit()
    conn.close()
