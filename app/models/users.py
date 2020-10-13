from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager



class User(UserMixin, db.Model):
    """
    Creacion de tabla users.
    """

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    @property
    def password(self):
        """
        Prevencion de acceso a la contraseña
        """
        raise AttributeError('No se puede leer la contraseña.')

    @password.setter
    def password(self, password):
        """
        Setter de contraseña por hash
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Verificacion de hash contraseña
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<user: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

permissions_roles = db.Table('permissions_roles', db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True), db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True))

class Role(db.Model):
    """
    Creacion de tabla Roles
    """

    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',lazy='dynamic')
    permissions = db.relationship('Permission', secondary=permissions_roles, back_populates='roles',lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Permission(db.Model):
    """
    Creacion de tabla Permisos
    """

    __tablename__ = 'permissions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(60), unique=True)
    allow = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=permissions_roles, back_populates='permissions',lazy='dynamic')
    def __repr__(self):
        return '<Permission: {}>'.format(self.action)

class Config(db.Model):
    """
    Creacion de tabla Configuracion
    """

    __tablename__ = 'config'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200))
    email = db.Column(db.String(60))
    n_elements = db.Column(db.Integer)
    site_enabled = db.Column(db.Boolean)

    def __repr__(self):
        return '<Config: {}>'.format(self.action)
