from flask import flash, redirect, session, render_template, url_for, Blueprint, request
from app.models.model import User, Role, Permission, users_roles, Config
from app.extensions import db
from app.admin.resources.forms import LoginForm, RegistrationForm, ConfigForm, EditForm
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


@admin_bp.route('/usuarios/registrar/', methods=['GET', 'POST'])
@login_required
def registrar_usuario():
    """
        CREATE
        Registar un nuevo usuario desde usuario admin
        ID 7 USER_NEW permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 7):
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
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/listar/', methods=['GET', 'POST'])
@login_required
def listar_usuarios():
    """
        READ
        Vista de modulo CRUD usuarios en administracion.
        ID 6 USER_INDEX permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.all()
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/activos')
@login_required
def usuarios_activos():
    """
        READ
        Devuelve una lista de los usuarios activos
        ID 6 USER_INDEX permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.filter_by(active=True)
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/bloqueados')
@login_required
def usuarios_bloqueados():
    """
        READ
        Devuelve una lista de los usuarios bloqueados
        ID 6 USER_INDEX permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.filter_by(active=False)
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/buscar/', methods=['GET', 'POST'])
@login_required
def buscar_por_nombre():
    """
        READ
        Devuelve una lista de usuarios con nombre enviado como parametro
        ID 6 USER_INDEX permisos
    """
    nombre = request.form.get('buscar-nombre')
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.filter_by(first_name=nombre)
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/activar/<id>', methods=['GET', 'POST'])
@login_required
def activar_bloquear(id):
    """
        READ
        Bloquea un usuario activo 
        /
        Activa un usuario bloqueado
        ID 9 USER_UPDATE permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 9):

        user_edit = User.query.filter_by(id=id).first()
        if not user_edit:
            flash('El usuario solicitado no existe.', 'danger')
            return redirect(url_for('admin.index'))

        user = User.query.get(id)
        user.active = not user.active
        db.session.commit()
        flash('Los cambios se guardaron correctamente.', 'success')
        return redirect(url_for('admin.listar_usuarios'))
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('/configuracion', methods=['GET', 'POST'])
@login_required
def configuracion():
    """
      Vista de configuracion de sistema en administracion.
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 10):
        # Trae la informacion ya cargada para mostrarla en el formulario cuando method=GET
        config = Config.query.first()
        if not config:
            form = ConfigForm()
            # Guarda la informacion cargada desde el template cuando method=POST
            if form.validate_on_submit():
                config = Config(
                    title=form.title.data,
                    description=form.description.data,
                    email=form.email.data,
                    n_elements=form.n_elements.data,
                    site_enabled=form.site_enabled.data)
                db.session.add(config)
                flash('Los cambios se guardaron correctamente.', 'success')
        else:
            form = ConfigForm(obj=config)
            # Guarda la informacion cargada desde el template cuando method=POST
            if form.validate_on_submit():
                form.populate_obj(config)
                flash('Los cambios se guardaron correctamente.', 'success')
        db.session.commit()
        return render_template('admin/configuracion.html', form=form, title='Centros de Ayuda GBA - Configuración')
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('usuarios/actualizar/<id_user>', methods=['GET', 'POST'])
@login_required
def actualizar_usuario(id_user):
    """
        Vista de actualizacion de un usuario enviado como parámetro con un usuario admin
        Requiere permiso con ID 9 (USER_UPDATE)
    """

    id_admin = current_user.get_id()
    if User.tiene_permiso(id_admin, 9):

        user_edit = User.query.filter_by(id=id_user).first()
        if not user_edit:
            flash('El usuario solicitado no existe.', 'danger')
            return redirect(url_for('admin.index'))

        roles = user_edit.roles.all()
        es_admin = Role.query.filter_by(name='admin').first() in roles
        es_operador = Role.query.filter_by(name='operador').first() in roles
        form = EditForm(obj=user_edit, id=id_user,
                        admin=es_admin, operator=es_operador)

        # POST.
        if form.validate_on_submit():
            form.populate_obj(user_edit)
            if form.admin.data:
                if not es_admin:
                    user_edit.roles.append(Role.query.get(1))
            elif es_admin:
                user_edit.roles.remove(Role.query.get(1))
            if form.operator.data:
                if not es_operador:
                    user_edit.roles.append(Role.query.get(2))
            elif es_operador:
                user_edit.roles.remove(Role.query.get(2))

            db.session.commit()
            # redirecciona al listado de usuarios
            flash('Los cambios se guardaron correctamente.', 'success')
            return redirect(url_for('admin.listar_usuarios'))

        return render_template('admin/update_user.html', form=form, title='Centros de Ayuda GBA - Configuración')
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('usuarios/borrar/<id>', methods=['GET', 'POST'])
@login_required
def eliminar_usuario(id):
    """
        Vista de eliminacion de un usuario, enviado como parámetro con sus relaciones, con un usuario admin
        Requiere permiso con ID8 (USER_DESTROY)
    """

    id_admin = current_user.get_id()
    if User.tiene_permiso(id_admin, 8):

        user_delete = User.query.filter_by(id=id).first()
        if not user_delete:
            flash('El usuario solicitado no existe.', 'danger')
            return redirect(url_for('admin.index'))

        db.session.delete(user_delete)
        db.session.commit()

        flash('El usuario se eliminó correctamente', 'success')
        return redirect(url_for('admin.listar_usuarios'))
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))
