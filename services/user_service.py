import bcrypt
import os
import sqlite3
from dotenv import load_dotenv
from utils.senhas import hash_password
from email_validator import validate_email, EmailNotValidError

load_dotenv()

class UserService:
    @staticmethod
    def create_user(nome, email,senha):
        senha_hashed = hash_password(senha)
        try:
            validate_email(email=email)
        except EmailNotValidError:
            return False
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            c = conn.cursor()
            c.execute("INSERT INTO user (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hashed))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
