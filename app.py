from flask import Flask, jsonify, session, redirect, url_for,render_template,request
import os
from dotenv import load_dotenv
from services.auth_service import AuthService
from services.user_service import UserService
from services.resident_service import ResidentService

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if AuthService.authenticate(email, password):
            session['user'] = email
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Credenciais inválidas')
        
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        if UserService.create_user(
            nome=request.form['nome'],
            email=request.form['email'],
            senha=request.form['password']
        ):
            return redirect(url_for('login'))
        else:
            return render_template('cadastro.html', error='Email já existe')
        
    return render_template('cadastro.html')

@app.route('/cadastro_residente', methods=['GET'])
def cadastro_residente():
    if 'user' not in session:
        return redirect(url_for('login'))
    residents = ResidentService.get_residents_by_session(session['user_id'])
    return render_template('cadastro_residente.html', residents=residents)

@app.route('/api/residents', methods=['POST'])
def add_residente():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        resident = request.form
        if ResidentService.create_resident(resident['nome'],resident['sobrenome'], session['user_id']):
            return jsonify({
                    "message": "Residente cadastrado com sucesso!",
                    "resident": {
                        
                        "nome": resident['nome'],
                        "sobrenome": resident['sobrenome']
                    }
                    }), 201
        else:
            return jsonify({'message': 'Erro ao cadastrar residente.'}), 400




@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)