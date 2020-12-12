from app.admin.resources.forms import LoginForm, RegistrationForm, ConfigForm, EditForm, HelpCenterForm, AppointmentForm, AppointmentWithCenterForm
from flask import flash, redirect, session, render_template, url_for, Blueprint, request, jsonify, make_response, current_app, abort
from app.models.model import User, Role, Permission, users_roles, Config, HelpCenter, Status, CenterType, Appointment, HelpCenterSchema, CenterTypeSchema, StatusSchema, AppointmentSchema
from app.extensions import db
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import or_
from os import path
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask_cors import cross_origin
import requests
import math
import decimal
import datetime
import json
import re
from email_validator import validate_email, EmailNotValidError
from app.admin.helpers.turnos import generar_turnos

# Blueprint Administracion
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
def index():
    """
        Renderizar la pagina principal de la administracion.
    """
    return render_template('admin/index.html')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AUTH ROUTES #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# USER ROUTES #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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
        return render_template('admin/usuarios.html', users=users, search=search)
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

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CRUD CENTROS DE AYUDA #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@admin_bp.route('listado_centros/', methods=['GET', 'POST'])
@admin_bp.route('listado_centros/<int:page>/', methods=['GET', 'POST'])
@login_required
def centros_ayuda(page=1):
    items_per_page = Config.query.first().n_elements
    centros = HelpCenter.query.paginate(page, per_page=items_per_page)
    return render_template('admin/centros.html', centros=centros)


@admin_bp.route('listado_centros/buscar/', methods=['GET', 'POST'])
@admin_bp.route('listado_centros/<int:page>/buscar', methods=['GET', 'POST'])
@login_required
def centros_buscar_nombre(page=1):
    search = request.form.get('buscar-centro')
    items_per_page = Config.query.first().n_elements
    centros = HelpCenter.query.filter(HelpCenter.name_center.contains(
        search)).paginate(page, per_page=items_per_page)
    return render_template('admin/centros.html', centros=centros, search=search)


@admin_bp.route('listado_centros/filtrar/', methods=['GET', 'POST'])
@admin_bp.route('listado_centros/filtrar/<int:page>', methods=['GET', 'POST'])
@login_required
def centros_filtrar_estado(page=1):
    items_per_page = Config.query.first().n_elements
    status = request.args.get('status')
    centros = HelpCenter.query.filter_by(
        status_id=status).paginate(page, per_page=items_per_page)
    return render_template('admin/centros.html', centros=centros)


@admin_bp.route('centro/<id>', methods=['GET', 'POST'])
@login_required
def ver_centro(id):
    # IMPLEMENTAR
    centro = HelpCenter.query.filter_by(id=id).first()
    return render_template('admin/centro.html', centro=centro)


@admin_bp.route('centro/crear', methods=['GET', 'POST'])
@login_required
def crear_centro():

    id_admin = current_user.get_id()
    if User.tiene_permiso(id_admin, 2):

        results = []
        response = requests.get(
            'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios').json()

        per_page = response['per_page']
        total = response['total']

        for page in range(1, math.ceil(total/per_page)+1):
            response = requests.get(
                'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios', params={'page': page}).json()
            data = response['data']
            municipios = data['Town']
            for v in municipios.values():
                results.append((v['name']))

        municipios_list = sorted(results)

        form = HelpCenterForm()
        form.town.choices = municipios_list
        form.center_type_id.choices = CenterType.query.with_entities(
            CenterType.id, CenterType.name_center_type).all()
        if form.validate_on_submit():
            protocol_path = ""
            if form.visit_protocol.data:
                protocol_file = form.visit_protocol.data
                filename_vp = secure_filename(protocol_file.filename)
                protocol_path = path.join(
                    current_app.root_path, 'static/uploads', filename_vp)
                protocol_file.save(protocol_path)
            help_center = HelpCenter(
                name_center=form.name_center.data,
                address=form.address.data,
                phone=form.phone.data,
                opening_time=form.opening_time.data,
                close_time=form.close_time.data,
                town=form.town.data,
                web=form.web.data,
                email=form.email.data,
                visit_protocol=protocol_path,
                status_id=1,
                center_type_id=form.center_type_id.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data
            )
            # agrega nuevo centro a la db.
            db.session.add(help_center)
            db.session.commit()

            # redirecciona a pagina login.
            return redirect(url_for('admin.centros_ayuda'))

        return render_template('admin/centro_edit.html', form=form)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('centro/actualizar/<id>', methods=['GET', 'POST'])
@ login_required
def actualizar_centro(id):

    id_admin = current_user.get_id()
    if User.tiene_permiso(id_admin, 4):

        results = []
        response = requests.get(
            'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios').json()

        per_page = response['per_page']
        total = response['total']

        for page in range(1, math.ceil(total/per_page)+1):
            response = requests.get(
                'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios', params={'page': page}).json()
            data = response['data']
            municipios = data['Town']
            for v in municipios.values():
                results.append((v['name']))

        municipios_list = sorted(results)

        current_center = HelpCenter.query.filter_by(id=id).first()
        current_protocol = current_center.visit_protocol
        current_protocol_name = str(current_protocol).split('/')[-1:][0]
        form = HelpCenterForm(obj=current_center)
        form.town.choices = municipios_list
        form.center_type_id.choices = CenterType.query.with_entities(
            CenterType.id, CenterType.name_center_type).all()
        if form.validate_on_submit():
            if form.visit_protocol.data != current_protocol:
                protocol_file = form.visit_protocol.data
                filename_vp = secure_filename(protocol_file.filename)
                protocol_path = path.join(
                    current_app.root_path, 'static/uploads', filename_vp)
                protocol_file.save(protocol_path)
                form.visit_protocol.data = protocol_path
            form.populate_obj(current_center)
            db.session.commit()
            flash('Los cambios se guardaron correctamente.', 'success')
            return redirect(url_for('admin.centros_ayuda'))
        return render_template('admin/centro_edit.html', form=form, current_protocol=current_protocol_name, edit_mode=True)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('centro/eliminar/<id>', methods=['GET', 'POST'])
@ login_required
def eliminar_centro(id):

    id_admin = current_user.get_id()
    if User.tiene_permiso(id_admin, 3):

        center_delete = HelpCenter.query.filter_by(id=id).first()
        if not center_delete:
            flash('El centro de ayuda solicitado no existe.', 'danger')
            return redirect(url_for('admin.centros_ayuda'))

        Appointment.query.filter_by(center_id=id).delete()
        db.session.delete(center_delete)
        db.session.commit()

        flash('El centro de ayuda se eliminó correctamente', 'success')
        return redirect(url_for('admin.centros_ayuda'))
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))

    return 'Borrado de Centro de ayuda'


@ admin_bp.route('centro/aceptar/<id>', methods=['GET', 'POST'])
@ login_required
def aceptar_centro(id):
    id_admin = current_user.get_id()
    if User.tiene_permiso(id_admin, 4):
        centro = HelpCenter.query.filter_by(id=id).first().status_id = 1
        db.session.commit()
        flash('Centro Aceptado', 'success')
        return redirect(url_for('admin.centros_ayuda'))
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('centro/rechazar/<id>', methods=['GET', 'POST'])
@ login_required
def rechazar_centro(id):
    id_admin = current_user.get_id()
    if User.tiene_permiso(id_admin, 4):
        centro = HelpCenter.query.filter_by(id=id).first().status_id = 3
        db.session.commit()
        flash('Centro Rechazado', 'success')
        return redirect(url_for('admin.centros_ayuda'))
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  CRUD TURNOS #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@ admin_bp.route('turnos/', methods=['GET', 'POST'])
@ admin_bp.route('turnos/<int:page>', methods=['GET', 'POST'])
@ login_required
def turnos(page=1):
    """
        READ
        Listar Todos los turnos reservados de los proximos tres dias.
        ID 1 CENTRO_INDEX permisos
    """
    usuarios_por_pag = Config.query.first().n_elements
    id_usuario = current_user.get_id()

    if User.tiene_permiso(id_usuario, 1):
        fecha_hoy = datetime.datetime.today().strftime('%Y-%m-%d')
        fecha_man = (datetime.datetime.today() +
                     datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        fecha_pas = (datetime.datetime.today() +
                     datetime.timedelta(days=2)).strftime('%Y-%m-%d')

        turnos_hoy = Appointment.query.filter_by(appointment_date=fecha_hoy)
        turnos_man = Appointment.query.filter_by(appointment_date=fecha_man)
        turnos_pas = Appointment.query.filter_by(appointment_date=fecha_pas)
        turnos = turnos_hoy.union(turnos_man, turnos_pas)

        turnos = turnos.paginate(
            page, per_page=usuarios_por_pag)
        return render_template('admin/turnos.html', turnos=turnos)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('turnos/buscar', methods=['GET', 'POST'])
@ admin_bp.route('turnos/buscar/<int:page>', methods=['GET', 'POST'])
@ login_required
def turnos_buscar(page=1):
    search_name = request.form.get('buscar-nombre')
    search_date = request.form.get('buscar-fecha')
    id_usuario = current_user.get_id()
    usuarios_por_pag = Config.query.first().n_elements
    if User.tiene_permiso(id_usuario, 1):
        if search_name:
            results = HelpCenter.query.filter(
                HelpCenter.name_center.contains(search_name)).with_entities(HelpCenter.id)
            help_centers_ids = [value for value, in results]
            turnos = Appointment.query.filter(
                Appointment.center_id.in_(help_centers_ids)).union(Appointment.query.filter(Appointment.email.contains(search_name)))

            if search_date:
                turnos = turnos.filter_by(
                    appointment_date=search_date)
        else:
            if search_date:
                turnos = Appointment.query.filter_by(
                    appointment_date=search_date)
            else:
                turnos = Appointment.query

        turnos = turnos.paginate(page, per_page=usuarios_por_pag)
        return render_template('admin/turnos.html', turnos=turnos, search_name=search_name, search_date=search_date)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('turnos/buscar/centro/<id>', methods=['GET', 'POST'])
@ admin_bp.route('turnos/buscar/centro/<id>/<int:page>', methods=['GET', 'POST'])
@ login_required
def turnos_centro_buscar(id=0, page=1):
    search_date = request.form.get('buscar-fecha')
    search_name = request.form.get('buscar-nombre')
    id_usuario = current_user.get_id()
    usuarios_por_pag = Config.query.first().n_elements
    centro = HelpCenter.query.filter_by(id=id).first()
    if User.tiene_permiso(id_usuario, 1):
        turnos = Appointment.query.filter_by(center_id=centro.id)
        if search_name:
            turnos = turnos.filter(Appointment.email.contains(search_name))
        if search_date:
            turnos = turnos.filter_by(
                appointment_date=search_date)
        turnos = turnos.paginate(page, per_page=usuarios_por_pag)
        return render_template('admin/turnos.html', turnos=turnos, search_date=search_date, search_name=search_name, centro=centro)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('centro/<id>/turnos', methods=['GET', 'POST'])
@ admin_bp.route('centro/<id>/turnos/<int:page>', methods=['GET', 'POST'])
@ login_required
def turnos_centro(id=0, page=1):
    id_usuario = current_user.get_id()
    usuarios_por_pag = Config.query.first().n_elements
    centro = HelpCenter.query.filter_by(id=id).first()
    if User.tiene_permiso(id_usuario, 1):
        turnos = Appointment.query.filter_by(
            center_id=centro.id).paginate(page, per_page=usuarios_por_pag)
        return render_template('admin/turnos.html', turnos=turnos, centro=centro)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('centro/turnos/crear', methods=['GET', 'POST'])
@admin_bp.route('centro/<int:id>/turnos/crear', methods=['GET', 'POST'])
@login_required
def crear_turno(id=0):
    """
        CREATE
        Registar un nuevo turno
        ID 12 TURNO_NEW permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 12):

        # Si recibe Id por paremetro no es necesario seleccionar el Centro. Sino, mostrar Selector de centros.
        if id > 0:
            centro = HelpCenter.query.get(id)
            centro_nombre = centro.name_center
            form = AppointmentForm()
        else:
            form = AppointmentWithCenterForm()
            centros_ayuda_aceptados = HelpCenter.query.filter_by(
                status_id=1).with_entities(HelpCenter.id, HelpCenter.name_center).all()
            form.center_id.choices = centros_ayuda_aceptados
            centro_nombre = ''
        # POST
        if form.validate_on_submit():

            if id > 0:
                appointment = Appointment(
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    phone=form.phone.data,
                    start_time=form.start_time.data,
                    appointment_date=form.appointment_date.data,
                    center_id=id
                )
            else:
                appointment = Appointment(
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    phone=form.phone.data,
                    start_time=form.start_time.data,
                    appointment_date=form.appointment_date.data,
                    center_id=form.center_id.data
                )
                centro = HelpCenter.query.get(form.center_id.data)

            delta = datetime.timedelta(minutes=30)
            start = appointment.start_time
            appointment.end_time = (datetime.datetime.combine(
                datetime.date(1, 1, 1), start) + delta).time()
            # Me trae el turno del centro recibido, con esa fecha y esa hora de inicio
            turnos_del_dia = Appointment.query.filter_by(
                center_id=id, appointment_date=appointment.appointment_date, start_time=appointment.start_time).first()
            if not turnos_del_dia:
                centro.appointments.append(appointment)
                db.session.commit()
                # redirecciona a pagina turnos del dia del centro
                # return redirect(url_for('admin.turnos_centro({})'.format(id)))
                flash('Turno creado exitosamente', 'success')
                return redirect(url_for('admin.turnos_centro', id=centro.id))
            else:
                flash('Turno no disponible', 'danger')
                return render_template('admin/turno_edit.html', form=form, center_name=centro_nombre, center_id=id, title='Centros de Ayuda GBA - Sacar turno')

        return render_template('admin/turno_edit.html', form=form, center_name=centro_nombre, center_id=id, title='Centros de Ayuda GBA - Sacar turno')
    else:
        flash('No tienes permisos para realizar esa acción', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('turnos/actualizar/<id>', methods=['GET', 'POST'])
@ login_required
def actualizar_turno(id):
    """
        UPDATE
        Actualiza un turno
        ID 14 TURNO_UPDATE permisos
    """
    id_admin = current_user.get_id()
    if User.tiene_permiso(id_admin, 14):
        turno_edit = Appointment.query.get(id)
        if not turno_edit:
            flash('El turno solicitado no existe.', 'danger')
            return redirect(url_for('admin.index'))
        centro = HelpCenter.query.get(turno_edit.center_id)
        centro_nombre = centro.name_center
        form = AppointmentForm(obj=turno_edit, id=id)

        # POST.
        if form.validate_on_submit():
            form.populate_obj(turno_edit)
            delta = datetime.timedelta(minutes=30)
            start = form.start_time.data
            turno_edit.end_time = (datetime.datetime.combine(
                datetime.date(1, 1, 1), start) + delta).time()
            # Me trae el turno del centro recibido, con esa fecha y esa hora de inicio
            turnos_del_dia = Appointment.query.filter_by(
                center_id=turno_edit.center_id, appointment_date=turno_edit.appointment_date, start_time=turno_edit.start_time)
            if turnos_del_dia.count() == 1:
                db.session.commit()
                # redirecciona al listado de usuarios
                flash('Los cambios se guardaron correctamente.', 'success')
                return redirect(url_for('admin.turnos_centro', id=centro.id))
            else:
                flash('Turno no disponible', 'danger')
                return render_template('admin/turno_edit.html', form=form, center_name=centro_nombre, title='Centros de Ayuda GBA - Actualizar turno')
        return render_template('admin/turno_edit.html', form=form, center_name=centro_nombre, center_id=centro.id, title='Centros de Ayuda GBA - Actualizar turno')
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('turnos/eliminar/<id>', methods=['GET', 'POST'])
@ login_required
def eliminar_turno(id):
    """
        DELETE
        Eliminar un turno
        ID 13 TURNO_DESTROY permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 13):

        turno = Appointment.query.get(id)
        if not turno:
            flash('El turno no existe.', 'danger')
            return redirect(url_for('admin_index'))

        db.session.delete(turno)
        db.session.commit()

        flash('El turno se eliminó correctamente.', 'success')
        return redirect(url_for('admin.turnos'))
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  API ROUTES #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@ admin_bp.route('/centros', methods=["GET", "POST"])
def api_centros():
    """
         API endpoint: /centros

         Method GET:
             Este servicio permite obtener TODOS los centros de ayuda.
         Method POST:
             Este servicio permite cargar UN centro de ayuda.

     """

    if request.method == 'GET':

        # Obtener todos los Centros de Ayuda #

        centers = HelpCenter.query.all()

        # Serializar a JSON los Centros de Ayuda #

        help_center_schema = HelpCenterSchema(many=True)
        output = help_center_schema.dump(centers)

        # Crear una respuesta HTTP 200 OK con el JSON de Centros de Ayuda #

        res = make_response(jsonify(output), 200, {
            'Content-Type': 'charset=utf-8'})

    elif request.method == 'POST':

        # Recibir un Centro de Ayuda en JSON #

        try:

            # Si el request es un JSON, obtenerlo para validar los datos #

            data = request.get_json()

            # Instancia HelpCenter validando que esten todas las claves correspondientes en el JSON #
            data["latitude"] = 0
            data["longitude"] = 0

            # validar Email
            validate_email(data["email"])

            # validar Horarios
            if not bool(re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$').match(data["opening_time"])):
                raise Exception("Horario de apertura invalido")
            if not bool(re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$').match(data["close_time"])):
                raise Exception("Horario de cierre invalido")

            help_center = HelpCenter(**{k: data[k] for k in ("name_center",
                                                             "address",
                                                             "phone",
                                                             "opening_time",
                                                             "close_time",
                                                             "town",
                                                             "web",
                                                             "email",
                                                             "visit_protocol",
                                                             "center_type_id",
                                                             "latitude",
                                                             "longitude") if k in data})

            # Actualiza BD con el nuevo Centro de Ayuda #

            db.session.add(help_center)
            db.session.commit()

            # Crea una respuesta HTTP 201 Created con el JSON del nuevo Centro de Ayuda #

            res = make_response(jsonify(data), 201, {
                                'Content-Type': 'application/json; charset=utf-8'})
        except EmailNotValidError:
            res = make_response(
                jsonify({"mensaje": "E-mail inválido."}), 400)
        except Exception:

            # Crea una respuesta HTTP 400 Bad Request si falla la creacion  #

            res = make_response(
                jsonify({"mensaje": "No se pudo cargar el centro de ayuda."}), 400)

    return res


@ admin_bp.route('/centros/<centro_id>', methods=["GET"])
def api_centro(centro_id):
    """
        API endpoint: /centros/id

        Method GET:
            Este servicio permite obtener UN centro de ayuda identificado por parametro ID.
            Respuestas: 200 OK
                        404 Not Found
                        500 Server Error

    """

    center = HelpCenter.query.filter_by(id=centro_id).first()

    if not center:
        abort(404)

    # Serializar a JSON los Centros de Ayuda #

    help_center_schema = HelpCenterSchema()
    output = help_center_schema.dump(center)

    # Crear una respuesta HTTP 200 OK con el JSON de Centros de Ayuda #

    return make_response(jsonify(output), 200, {'Content-Type': 'application/json; charset=utf-8'})


@ admin_bp.route('/centros/<centro_id>/turnos_disponibles', methods=["GET"])
@ cross_origin()
def api_centro_turnos(centro_id):
    """
         API endpoint: /centros/<centro_id>/turnos_disponibles/?fecha=<fecha>

         Method GET:
             Este servicio permite obtener el listado de los turnos disponibles
             para UN centro de ayuda en un dia en particular
        Parametros:
            ID del centro
        Query String:
            fecha: YY-MM-DD (ej:2020-12-01)

    """
    center = HelpCenter.query.filter_by(id=centro_id).first()

    if not center:
        abort(404)

    data = {}
    data['appointments'] = []
    delta = datetime.timedelta(minutes=30)
    # date toma el dia pasado, si no se pasa el argumento toma el dia de hoy
    fecha = request.args.get('fecha')
    
    if fecha:
        date = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    else:
        date = datetime.date.today()

    todos_los_turnos = generar_turnos(center.opening_time, center.close_time)

    # Filtro los turnos del dia del centro recibido
    turnos_del_dia = Appointment.query.filter_by(
        center_id=centro_id, appointment_date=date).all()
    for turno in turnos_del_dia:
        todos_los_turnos.remove(turno.start_time)
    for turno in todos_los_turnos:
        fin = (datetime.datetime.combine(
            datetime.date(1, 1, 1), turno) + delta).time()
        data['appointments'].append({
            'center_id': int(centro_id),
            'start_time': turno.strftime("%H:%M"),
            'end_time': fin.strftime("%H:%M"),
            'appointment_date': date.strftime('%Y-%m-%d')
        })
    a = json.dumps(data, sort_keys=False)
    # Crear una respuesta HTTP 200 OK con el JSON de Turnos del dia #

    res = make_response(a, 200, {
        'Content-Type': 'application/json; charset=utf-8'})

    return res


@ admin_bp.route('/centros/<centro_id>/reserva', methods=["POST"])
@ cross_origin()
def api_centro_reserva(centro_id):
    """
         API endpoint: /centros/<centro_id>/reserva

         Method POST:
             Este servicio permite realizar una reserva de un turno para un centro de ayuda
             en un dia en particular
         Parametros:
            ID del Centro

    """
    try:
        if not HelpCenter.query.filter_by(id=centro_id).first():
            raise Exception("El centro de ayuda no existe.")
        data = request.get_json()

        # validar formato Horarios
        
        if type(data["start_time"]) != str or not bool(re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$').match(data["start_time"])):
            raise Exception("Horario de apertura invalido")
        if type(data["end_time"]) != str or not bool(re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$').match(data["end_time"])):
            raise Exception("Horario de cierre invalido")

        center_accepted = HelpCenter.query.filter_by(
            id=centro_id).filter_by(status_id=1).first()

        opening_center = HelpCenter.query.filter_by(
            id=centro_id).first().opening_time
        close_center = HelpCenter.query.filter_by(
            id=centro_id).first().close_time

        request_start = datetime.datetime.strptime(
            data["start_time"], '%H:%M').time()
        request_end = datetime.datetime.strptime(
            data["end_time"], '%H:%M').time()

        appointment_start = request_start
        appointment_end = request_end

        exists = Appointment.query.filter_by(center_id=centro_id).filter_by(
            appointment_date=data["appointment_date"]).filter_by(start_time=data["start_time"]).first()

        # validar formato Email
        
        validate_email(data["email"])


        # validar estado del centro

        if not center_accepted:
            raise Exception("El centro de ayuda no está disponible.")
        
        # validar franjas horarias

        if not (appointment_start >= opening_center and appointment_end <= close_center):
            raise Exception(
                "El horario solicitado está fuera del rango del horario de atención.")
        correct_end = (datetime.datetime.combine(datetime.date(
            1, 1, 1), request_start)+datetime.timedelta(minutes=30)).time()
        if not (correct_end == request_end):
            raise Exception("Los bloques deben ser de 30 minutos.")
        if exists:
            raise Exception("El turno solicitado ya está reservado.")
        appointment = Appointment(**{k: data[k] for k in ("email",
                                                          "first_name",
                                                          "last_name",
                                                          "phone",
                                                          "start_time",
                                                          "end_time",
                                                          "appointment_date",
                                                          "center_id"
                                                          ) if k in data})

        db.session.add(appointment)
        db.session.commit()
        res = make_response(jsonify(data), 201, {
            'Content-Type': 'application/json; charset=utf-8'})

    except EmailNotValidError:
        res = make_response(
            jsonify({"mensaje": "E-mail inválido."}), 400)
    except Exception as err:
        res = make_response(
            jsonify({"mensaje": str(err)}), 400)

    return res
