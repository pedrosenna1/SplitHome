import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class ResidentService:
    @staticmethod
    def create_resident(name,sobrenome,session_id):
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            c = conn.cursor()
            c.execute("INSERT INTO resident (name, sobrenome, session_id) VALUES (?, ?, ?)", (name, sobrenome, session_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        
    @staticmethod
    def get_residents_by_session(session_id):
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT id, name, sobrenome FROM resident WHERE session_id = ?", (session_id,))
            residents = c.fetchall()
            conn.close()
            return residents
        except sqlite3.Error:
            return []
        
        