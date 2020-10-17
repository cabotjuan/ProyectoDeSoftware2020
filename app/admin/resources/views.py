from flask import flash, redirect, session, render_template, url_for, Blueprint
from app.models.model import User, Role, Permission, users_roles, Config
from app.extensions import db
from app.admin.resources.forms import LoginForm, RegistrationForm, ConfigForm
from flask_login import login_required, login_user, logout_user, current_user

# Blueprint Administracion
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def index():
    """
        Renderizar la pagina principal de la administracion.
    """
    return render_template('admin/index.html')

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
            # CARGAR PERMISOS EN SESION.
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


@admin_bp.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
    """
        Vista de modulo CRUD usuarios en administracion.
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario,6):
        users =User.query.all()
        return render_template('admin/usuarios.html', users=users)
    return render_template('admin/index.html')

@admin_bp.route('usuarios/registrar/', methods=['GET', 'POST'])
@login_required
def registrar_usuario():
    """
        Registar un nuevo usuario desde usuario admin
        ID 7 USER_NEW permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario,7):
        form = RegistrationForm()

        # POST.
        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                active=form.active.data,
                password=form.password.data)
            if form.admin.data:
                user.roles.append(Role.query.get(1))
            if form.operator.data:
                user.roles.append(Role.query.get(2))
            # agrega nuevo user a la db.
            db.session.add(user)
            db.session.commit()

            # redirecciona a pagina login.
            return redirect(url_for('admin.listar_usuarios'))
    return render_template('admin/register.html', form=form, title='Centros de Ayuda GBA - Registro')


@admin_bp.route('/usuarios/listar/', methods=['GET', 'POST'])
@login_required
def listar_usuarios():
    """
       Vista de modulo CRUD usuarios en administracion.
       ID 6 USER_INDEX permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario,6):
        users = User.query.all()
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.', 'piola')
        # danger ROJO
        # warning NARANJA
        # success VERDE
        return redirect(url_for('admin.index'))

@admin_bp.route('/usuariosactivos')
@login_required
def usuariosActivos():
    """
       Vista de los usuarios activos
    """
    users = User.get_by_active()
    return render_template('admin/usuarios.html', users=users)

@admin_bp.route('/usuariosbloqueados')
@login_required
def usuariosBloqueados():
    """
       Vista de los usuarios activos
    """
    users = User.get_by_blocked()
    return render_template('admin/usuarios.html', users=users)

@admin_bp.route('/configuracion', methods=['GET', 'POST'])
@login_required
def configuracion():
    """
      Vista de configuracion de sistema en administracion.
    """
    # Trae la informacion ya cargada para mostrarla en el formulario cuando method=GET
    config = Config.query.first()
    form = ConfigForm(obj=config)

    # Guarda la informacion cargada desde el template cuando method=POST
    if form.validate_on_submit():
       form.populate_obj(config) 
       db.session.commit()
       
    # Carga login template
    return render_template('admin/configuracion.html', form=form, title='Centros de Ayuda GBA - Configuración')


















@admin_bp.route('/usuarios/habilitar/<id>', methods=['GET', 'POST'])
@login_required
def actualizar_usuario(id):
    
    return id





















""" @admin_bp.route('usuarios/<nombre>', methods=['GET', 'POST'])
@login_required
def buscar_por_nombre():
        READ
        Devuelve una lista de usuarios con nombre enviado como parametro
        ID 6 USER_INDEX permisos
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.filter_by(first_name=first_name)
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.')
        return render_template(url_for('admin.index'))


@admin_bp.route('/usuariosactivos')
@login_required
def usuariosActivos():
        READ
        Devuelve una lista de los usuarios activos
        ID 6 USER_INDEX permisos
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.filter_by(active=True)
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.')
        return render_template(url_for('admin.index'))


@admin_bp.route('/usuariosbloqueados')
@login_required
def usuariosBloqueados():

        READ
        Devuelve una lista de los usuarios bloqueados
        ID 6 USER_INDEX permisos
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.filter_by(active=False)
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.')
        return render_template(url_for('admin.index'))
 """
