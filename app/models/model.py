from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.extensions import login_manager

users_roles = db.Table('users_roles', db.Column('role_id', db.Integer, db.ForeignKey(
    'roles.id'), primary_key=True), db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True))

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
    active = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role', secondary=users_roles,
                            back_populates='users', lazy='dynamic')

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

    @staticmethod
    def tiene_permiso(id_usuario, id_permiso):
        """
        devuelve si el usuario tiene el permiso enviado
        """
        user = User.query.filter_by(id=id_usuario).first()
        roles = user.roles
        permiso = roles.filter(Role.permissions.any(id=id_permiso)).all()
        return len(permiso) != 0


    @staticmethod
    def get_by_name(first_name):
        """
        Devuelve una lista de usuarios con first_name igual al parametro
        """
        return User.query.filter_by(first_name=first_name)

    @staticmethod
    def get_by_active():
        """
        Devuelve una lista de los usuarios activos
        """
        return User.query.filter_by(active=True)

    @staticmethod
    def get_by_blocked():
        """
        Devuelve una lista de los usuarios bloqueados
        """
        return User.query.filter_by(active=False)

    @staticmethod
    def all():
        """
        Devuelve todos los usuarios del sistema
        """
        return User.query.all()


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
    users = db.relationship(
        'User', secondary=users_roles, back_populates='roles', lazy='dynamic')
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