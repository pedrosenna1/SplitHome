from flask import Flask, jsonify, session, redirect, url_for,render_template,request
import os
from dotenv import load_dotenv
from services.auth_service import AuthService
from services.user_service import UserService
from services.resident_service import ResidentService
from services.conta_service import ContaService
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=6)

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
            tokens = AuthService.tokens(email, password)
            if tokens:
                print(tokens)
                session['access_token'] = tokens.get('access_token')
                session['refresh_token'] = tokens.get('refresh_token')
                return redirect(url_for('home'))
            
            return render_template('login.html', error='Erro ao obter tokens')
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
        if ResidentService.create_resident(resident['nome'],resident['sobrenome'],resident['email'], resident['telefone'], session['user_id']):
            return jsonify({
                    "message": "Residente cadastrado com sucesso!",
                    "resident": {
                        
                        "nome": resident['nome'],
                        "sobrenome": resident['sobrenome'],
                        'email': resident['email'],
                        'telefone': resident['telefone']
                    }
                    }), 201
        else:
            return jsonify({'message': 'Erro ao cadastrar residente.'}), 400
        
@app.route('/api/residents/<int:resident_id>', methods=['DELETE'])
def delete_residente(resident_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    if ResidentService.deletar_resident(resident_id):
        return jsonify({'message': 'Residente deletado com sucesso.'}), 200
    else:
        return jsonify({'message': 'Erro ao deletar residente.'}), 400
    
@app.route('/contas')
def contas():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('contas.html')

@app.route('/api/get_contas', methods=['GET'])
def get_contas():
    if 'user' not in session:
        return redirect(url_for('login'))
    contas = ContaService.get_contas_by_user(session['user_id'])
    return jsonify(contas)

@app.route('/api/criar_conta', methods=['POST'])
def criar_conta():
    if 'user' not in session:
        return redirect(url_for('login'))
    data = request.json
    if ContaService.criar_conta(
        nome_conta=data.get('nome_conta'),
        valor=data.get('valor'),
        data_vencimento=data.get('data_vencimento'),
        categoria=data.get('categoria'),
        pago=data.get('pago', False),
        lembrete=data.get('lembrete', False),
        session_id=session['user_id']
    ):
        return jsonify({'message': 'Conta criada com sucesso.'}), 201
    else:
        return jsonify({'message': 'Erro ao criar conta.'}), 400
    
@app.route('/api/add_categoria', methods=['POST'])
def add_categoria():
    if 'user' not in session:
        return redirect(url_for('login'))
    nome_categoria = request.json.get('nome_categoria')
    if ContaService.adicionar_categoria(session['user_id'], nome_categoria):
        return jsonify({f'message': f'Categoria {nome_categoria} adicionada com sucesso.'}), 201
    else:
        return jsonify({'message': 'Erro ao adicionar categoria.'}), 400
    
@app.route('/api/get_categorias', methods=['GET'])
def get_categorias():
    if 'user' not in session:
        return redirect(url_for('login'))
    categorias = ContaService.get_categorias_by_user(session['user_id'])
    
    return jsonify(categorias)

@app.route('/api/pagar_conta', methods=['POST'])
def pagar_conta():
    if 'user' not in session:
        return redirect(url_for('login'))
    data = request.json
    conta_id = data.get('conta_id')
    if ContaService.pagar_conta(conta_id):
        return jsonify({'message': 'Conta marcada como paga com sucesso.'}), 200
    else:
        return jsonify({'message': 'Erro ao marcar conta como paga.'}), 400

@app.route('/api/get_contas_pendentes', methods=['GET'])
def get_contas_pendentes():
    if 'user' not in session:
        return redirect(url_for('login'))
    ano_mes = request.args.get('ano_mes')
    contas_pendentes = ContaService.get_contas_pendentes(session['user_id'], ano_mes)
    return jsonify(contas_pendentes)

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
    app.run()