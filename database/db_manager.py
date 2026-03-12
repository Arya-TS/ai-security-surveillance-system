import sqlite3

DB_NAME = "security_logs.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        timestamp TEXT,
        image_path TEXT,
        video_path TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS unknown_faces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        image_path TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_alert(name, timestamp, image_path, video_path):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO alerts (name, timestamp, image_path, video_path) VALUES (?, ?, ?, ?)",
        (name, timestamp, image_path, video_path)
    )

    conn.commit()
    conn.close()


def insert_unknown(timestamp, image_path):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO unknown_faces (timestamp, image_path) VALUES (?, ?)",
        (timestamp, image_path)
    )

    conn.commit()
    conn.close()