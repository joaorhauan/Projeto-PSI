import os
from flask import Flask
from config import db
from config import lm
from flask_migrate import Migrate
from app.controllers.user import user_bp # importa o blueprint do usuário
from app.controllers.home import home_bp # importa o blueprint da home

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # tipo de banco de dados sqlite, que criará um arquivo localmente
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # desativa o rastreamento de modificações do SQLAlchemy - consome bastante memória quando true, pois monitoria todas as modificações no banco de dados


    db.init_app(app) # inicializa o banco de dados
    migrate = Migrate(app, db)
    migrate.init_app(app, db) # inicializa o migrate
    lm.init_app(app) # inicializa o login manager
    

    app.register_blueprint(user_bp, url_prefix='/user') # registra o blueprint do usuário
    app.register_blueprint(home_bp)

    with app.app_context():
        db.create_all() # cria todas as tabelas no banco de dados

    return app