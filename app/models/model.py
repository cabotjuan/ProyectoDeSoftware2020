from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.extensions import login_manager
from app.extensions import ma

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

class HelpCenter(db.Model):
    __tablename__ ='help_centers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name_center = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    opening_time = db.Column(db.Time(), nullable=False)
    close_time = db.Column(db.Time(), nullable=False)
    town = db.Column(db.String(20), nullable=False)
    web = db.Column(db.String(80))
    email = db.Column(db.String(40))
    visit_protocol = db.Column(db.String(256))
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), default=2)
    center_type_id = db.Column(db.Integer, db.ForeignKey('center_types.id'))
    latitude = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.String(20), nullable=False)
    appointments = db.relationship('Appointment', backref='help_centers',lazy='dynamic')

class Status(db.Model):
    __tablename__ ='statuses'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name_status = db.Column(db.String(20), nullable=False)
    help_centers = db.relationship('HelpCenter', backref='statuses',lazy='dynamic')

class CenterType(db.Model):
    __tablename__ ='center_types'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name_center_type = db.Column(db.String(30), nullable=False)
    help_centers = db.relationship('HelpCenter', backref='center_types',lazy='dynamic')

class Appointment(db.Model):
    __tablename__ ='appointments'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True)    
    start_time = db.Column(db.Time(), nullable=False)
    end_time = db.Column(db.Time(), nullable=False)
    appointment_date = db.Column(db.Date(), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('help_centers.id'))


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class HelpCenterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HelpCenter

class CenterTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CenterType

class StatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Status

class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment