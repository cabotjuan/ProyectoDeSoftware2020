from flask import flash, redirect, render_template, url_for, Blueprint
from app.models.model import User
from app.extensions import db
from app.admin.resources.forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, logout_user

# Blueprint Administracion
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def index():
    """
        Renderizar la pagina principal de la administracion.
    """
    return render_template('admin/index.html')


@admin_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
        Registrar un nuevo usuario (rol_id 1 es admin) con RegistrationForm. Redirige a vista Login.
    """
    form = RegistrationForm()

    # POST.
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            role_id=1)
        # agrega nuevo user a la db.
        db.session.add(user)
        db.session.commit()

        # redirecciona a pagina login.
        return redirect(url_for('admin.login'))

    # GET. carga template registro.
    return render_template('admin/register.html', form=form, title='Centros de Ayuda GBA - Registro')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
        Autenticar usuario con LoginForm. Si es valido, redirige a Administracion. 
    """
    form = LoginForm()
    if form.validate_on_submit():
        # Verificar email en db
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # Autenticar usuario y redireccioinar a la Administracion
            login_user(user)
            return redirect(url_for('admin.index'))

    # Carga login template
    return render_template('admin/login.html', form=form, title='Centros de Ayuda GBA - Iniciar Sesion')


@admin_bp.route('/logout')
@login_required
def logout():
    """
        Finalizar sesion de usuario y redireccionar a Login.
    """
    logout_user()
    return redirect(url_for('admin.login'))


@admin_bp.route('/usuarios')
@login_required
def usuarios():
    """
       Vista de modulo CRUD usuarios en administracion.
    """
    #IMPLEMENTAR...
    return render_template('admin/usuarios.html')

@admin_bp.route('/configuracion')
@login_required
def configuracion():
    """
      Vista de configuracion de sistema en administracion.
    """
    #IMPLEMENTAR...
    return render_template('admin/configuracion.html')
