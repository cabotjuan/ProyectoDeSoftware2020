from flask import flash, redirect, session, render_template, url_for, Blueprint, request, jsonify, make_response
from app.models.model import User , Role, Permission, users_roles, Config
from app.extensions import db
from app.admin.resources.forms import LoginForm, RegistrationForm, ConfigForm, EditForm
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import or_
import requests
# Blueprint Administracion
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def index():
    """
        Renderizar la pagina principal de la administracion.
    """
    return render_template('admin/index.html')

# AUTH ROUTES #

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
            # Verificar si usuario esta deshabilitado
            if not user.active:
                flash('Tu cuenta ha sido deshabilitada.', 'danger')
                return redirect(url_for('admin.login'))

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


# USER ROUTES #

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
@admin_bp.route('/usuarios/listar/<int:page>', methods=['GET', 'POST'])
@login_required
def listar_usuarios(page=1):
    """
        READ
        Vista de modulo CRUD usuarios en administracion.
        ID 6 USER_INDEX permisos
    """
    usuarios_por_pag = Config.query.first().n_elements
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.paginate(page, per_page=usuarios_por_pag)
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/activos')
@admin_bp.route('/usuarios/activos/<int:page>')
@login_required
def usuarios_activos(page=1):
    """
        READ
        Devuelve una lista de los usuarios activos
        ID 6 USER_INDEX permisos
    """
    usuarios_por_pag = Config.query.first().n_elements
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.filter_by(active=True).paginate(
            page, per_page=usuarios_por_pag)
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/bloqueados')
@admin_bp.route('/usuarios/bloqueados/<int:page>')
@login_required
def usuarios_bloqueados(page=1):
    """
        READ
        Devuelve una lista de los usuarios bloqueados
        ID 6 USER_INDEX permisos
    """
    usuarios_por_pag = Config.query.first().n_elements
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.filter_by(active=False).paginate(
            page, per_page=usuarios_por_pag)
        return render_template('admin/usuarios.html', users=users)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@admin_bp.route('/usuarios/buscar/', methods=['GET', 'POST'])
@admin_bp.route('/usuarios/buscar/<int:page>', methods=['GET', 'POST'])
@login_required
def buscar_por_nombre(page=1):
    """
        READ
        Devuelve una lista de usuarios con nombre enviado como parametro
        ID 6 USER_INDEX permisos
    """
    usuarios_por_pag = Config.query.first().n_elements
    search = request.form.get('buscar-nombre')
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 6):
        users = User.query.filter(or_(User.first_name.contains(
            search), User.last_name.contains(search))).paginate(page, per_page=usuarios_por_pag)
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


# CRUD CENTROS DE AYUDA #


@admin_bp.route('listado_centros', methods=['GET', 'POST'])
@login_required
def centros_ayuda():
    return render_template('admin/centros_ayuda.html')


@admin_bp.route('listado_centros/', methods=['GET'])
@login_required
def centros_buscar_nombre():
    search = request.args.get('buscar-nombre')
    return render_template('admin/centros_ayuda.html',search=search)


@admin_bp.route('listado_centros/status=<status>', methods=['GET', 'POST'])
@login_required
def centros_filtrar_estado(status):
    return render_template('admin/centros_ayuda.html')


@admin_bp.route('centro/<id>', methods=['GET', 'POST'])
@login_required
def ver_centro(id):
    return render_template('admin/centro.html')


@admin_bp.route('centro/crear', methods=['GET', 'POST'])
@login_required
def crear_centro():
    return render_template('admin/centro_edit.html')


@admin_bp.route('centro/actualizar/<id>', methods=['GET', 'POST'])
@login_required
def actualizar_centro(id):
    return render_template('admin/centro_edit.html')


@admin_bp.route('centro/eliminar/<id>', methods=['GET', 'POST'])
@login_required
def eliminar_centro(id):
    return 'Borrado de Centro de ayuda'



#  CRUD TURNOS #



@admin_bp.route('turnos', methods=['GET', 'POST'])
@login_required
def turnos():
    return render_template('admin/turnos.html')

@admin_bp.route('turnos/centro=<search>', methods=['GET', 'POST'])
@login_required
def turnos_buscar_centro(search):
    return render_template('admin/turnos.html')

@admin_bp.route('turnos/email=<search>', methods=['GET', 'POST'])
@login_required
def turnos_buscar_email(search):
    return render_template('admin/turnos.html')

@admin_bp.route('centro/<id>/turnos', methods=['GET', 'POST'])
@login_required
def turnos_centro(id):
    return render_template('admin/turnos.html')

@admin_bp.route('centro/<id>/turnos/crear', methods=['GET', 'POST'])
@login_required
def crear_turno():
    return render_template('admin/turnos_edit.html')

@admin_bp.route('centro/<id>/turnos', methods=['GET', 'POST'])
@login_required
def actualizar_turno(id):
    return render_template('admin/turno_edit.html')

@admin_bp.route('centro/<id>/turnos', methods=['GET', 'POST'])
@login_required
def eliminar_turno(id):
    return 'Borrado de Turno'



#  API ROUTES #


@admin_bp.route('/centros', methods=["GET","POST"])
def api_centros():
    return 'response'


@admin_bp.route('/centros/<centro_id>', methods=["GET"])
def api_centro(centro_id):
    return 'response'


@admin_bp.route('/centros/<centro_id>/turnos_disponibles/', methods=["GET"])
def api_centro_turnos(centro_id):
    # /../?fecha=<fecha>
    #  SE DEBERIA USAR request.args.get('fecha')...
    return 'response'

@admin_bp.route('/centros/<centro_id>/reserva', methods=["POST"])
def api_centro_reserva(centro_id):
    return 'response'


#  TESTING ROUTES #

# ... # 
