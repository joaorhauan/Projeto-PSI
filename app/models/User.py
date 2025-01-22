from config import db
from flask_login import UserMixin

class User(db.Model, UserMixin): # UserMixin para usar o login
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True, name='email')
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) # Coluna do banco de dados para verificar se o usuário é admin

    def __init__(self, name, email, password, is_admin=False): # is admin false como padrão, pois se o valor não for passado, o usuário não é admin
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return f'<User {self.name}>'







     
