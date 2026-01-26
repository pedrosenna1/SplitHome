import bcrypt

def hash_password(senha):
    senha = senha.encode('utf-8')
    return bcrypt.hashpw(senha, bcrypt.gensalt())

def check_password(senha, hashed):
    senha = senha.encode('utf-8')
    return bcrypt.checkpw(senha, hashed)