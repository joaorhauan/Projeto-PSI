from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from app.models.User import User # importa a tabela de usuários
from config import db, lm
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user_bp', __name__)

# user_loader
@lm.user_loader
def load_user(id):
    return User.query.get(id)

@user_bp.route('/')
def index():
    usuarios = User.query.all() # comando para pegar todos os usuários no banco de dados
    return jsonify(usuarios) # retorna todos os usuários em formato json, por enquanto

@user_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        data = request.form # pega os dados do usuário

        if User.query.filter_by(email=data['email']).first():
            flash('Email já cadastrado')
            return redirect(url_for('user_bp.create'))

        
        hashed_password = generate_password_hash(data['password'])
        is_admin = data.get('is_admin') == 'on' # verifica se o checkbox está de admin está marcado, se sim define como true
        user = User(name=data['name'], email=data['email'], password=hashed_password, is_admin=is_admin) # cria um novo usuário
        db.session.add(user) 
        db.session.commit() # salva as alterações no banco de dados
        login_user(user) 
        return redirect(url_for('home_bp.index'))
    else:
        return render_template('user/create.html') 

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            login_user(user)
            return redirect(url_for('home_bp.index'))
        else:
            flash('Email ou senha incorretos')
            return redirect(url_for('user_bp.login'))
    else:
        return render_template('user/login.html')

@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))


