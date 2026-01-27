import sqlite3
from dotenv import load_dotenv
import os
import bcrypt
from utils.senhas import check_password
from flask import session


load_dotenv()

class AuthService:
    @staticmethod
    def authenticate(email, senha):
        conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT id,senha,perfil FROM user WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()
        if user:
            stored_password = user['senha']  # Assuming senha is the 2nd column
            if check_password(senha, stored_password):
                session['user_id'] = user['id']  # Store user ID in session
                session['perfil'] = user['perfil']  # Store user profile in session
                return True
            else:
                return False
        return False
        