import sqlite3
import os
from dotenv import load_dotenv
from utils.email_validador import is_valid_email

load_dotenv()

class ResidentService:
    @staticmethod
    def create_resident(name: str,sobrenome: str, email: str, telefone: str, session_id: int) -> bool:
        if not is_valid_email(email):
            return False
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            c = conn.cursor()
            c.execute("INSERT INTO resident (nome, sobrenome, email, telefone, user_id) VALUES (?, ?, ?, ?, ?)", (name, sobrenome, email, telefone, session_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
        
    @staticmethod
    def get_residents_by_session(session_id: int):
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            c.execute("SELECT id, nome, sobrenome, email, telefone FROM resident WHERE user_id = ?", (session_id,))
            residents = c.fetchall()
            conn.close()
            
            return residents
        except sqlite3.Error:
            conn.close()
            return []
        
    @staticmethod
    def deletar_resident(resident_id: int) -> bool:
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            c = conn.cursor()
            c.execute("DELETE FROM resident WHERE id = ?", (resident_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            conn.close()
            return False

        