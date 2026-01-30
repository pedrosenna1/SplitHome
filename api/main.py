from fastapi import FastAPI,HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Dict,List,Optional,Union
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv
import os
import sqlite3
import bcrypt

load_dotenv()


app = FastAPI()

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl='/api/autenticador', scopes={})

def check_password(senha, hashed):
    senha = senha.encode('utf-8')
    return bcrypt.checkpw(senha, hashed)

class AuthService:
    @staticmethod
    def authenticate(email, senha):
        try:
            conn = sqlite3.connect(f'../{os.getenv("DATABASE_PATH")}')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT id,senha,perfil FROM user WHERE email = ?", (email,))
            user = c.fetchone()
            conn.close()
            if user:
                try:
                    resp = check_password(senha,user['senha'])
                    if resp:
                        return {
                            'id': user['id'],
                            'email': email
                                }
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 


@app.post('/api/autenticador', status_code=status.HTTP_200_OK)
async def criar_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthService.authenticate(form_data.username,form_data.password)
    if user:
        payload = {
            'id': user['id'],
            'exp': datetime.now(timezone.utc) + timedelta(minutes=1),
            'token_use': 'access_token'
        }
        payload2 = {
            'id': user['id'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=8),
            'token_use': 'refresh_token'
        }
        try:
            access_token = jwt.encode(payload=payload,key=os.getenv('JWT_SECRET'),algorithm='HS256')
            refresh_token = jwt.encode(payload=payload2,key=os.getenv('JWT_SECRET'),algorithm='HS256')

            return {'access_token': access_token,
                    'refresh_token': refresh_token
                    }
        except:
            return {'message': 'Não foi possivel gerar o token'}
        
@app.get('/api/get', status_code=status.HTTP_200_OK)
async def get(token: str =  Depends(oauth2_scheme)):
    try:

        resp = jwt.decode(token,key=os.getenv('JWT_SECRET'),algorithms=['HS256'])

        if resp.get("token_use") != "access_token":
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return resp
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Token expirado.')
    

@app.get('/api/refresh')
async def refresh_token(token: str = Depends(oauth2_scheme)):
    try:

        resp = jwt.decode(token,key=os.getenv('JWT_SECRET'),algorithms=['HS256'])
        
        if resp['token_use'] == 'refresh_token':
            payload = {
            'id': resp['id'],
            'exp': datetime.now(timezone.utc) + timedelta(minutes=1),
            'token_use': 'access_token'
        }
            
            token = jwt.encode(payload=payload,key=os.getenv('JWT_SECRET'),algorithm='HS256')

            return {'access_token': token}
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token incorreto')
        
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Erro')
    




    
    



