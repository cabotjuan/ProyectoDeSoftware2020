from flask import flash, redirect, session, render_template, url_for, Blueprint, request, jsonify, make_response, current_app, abort
from app.models.model import User, Role, Permission, users_roles, Config, HelpCenter, Status, CenterType, Appointment, HelpCenterSchema, CenterTypeSchema, StatusSchema, AppointmentSchema, UserSchema
from app.extensions import db
from app.admin.resources.forms import LoginForm, RegistrationForm, ConfigForm, EditForm
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import or_
import requests
import math
import decimal
import datetime
import json

# Blueprint Administracion
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
def index():
    """
        Renderizar la pagina principal de la administracion.
    """
    print(current_app.config['UPLOAD_FOLDER'])
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


# CRUD CENTROS DE AYUDA #


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

    lista_municipios = sorted(results)

    return render_template('admin/centro_edit.html', municipios=lista_municipios)


@ admin_bp.route('centro/actualizar/<id>', methods=['GET', 'POST'])
@ login_required
def actualizar_centro(id):

    # IMPLEMENTAR

    return render_template('admin/centro_edit.html')


@ admin_bp.route('centro/eliminar/<id>', methods=['GET', 'POST'])
@ login_required
def eliminar_centro(id):

    # IMPLEMENTAR

    return 'Borrado de Centro de ayuda'


#  CRUD TURNOS #


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
@ admin_bp.route('turnos/<int:page>/buscar/', methods=['GET', 'POST'])
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
                Appointment.center_id.in_(help_centers_ids))
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
def turnos_centro_buscar(id,page=1):
    search_date = request.form.get('buscar-fecha')
    id_usuario = current_user.get_id()
    usuarios_por_pag = Config.query.first().n_elements
    centro = HelpCenter.query.filter_by(id=id).first()
    if User.tiene_permiso(id_usuario, 1):
        turnos = Appointment.query.filter_by(center_id=centro.id)
        if search_date:
            turnos=turnos.filter_by(
                appointment_date=search_date)
        turnos = turnos.paginate(page, per_page=usuarios_por_pag)
        return render_template('admin/turnos.html', turnos=turnos, search_date=search_date, centro=centro)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('centro/<id>/turnos', methods=['GET', 'POST'])
@ login_required
def turnos_centro(id,page=1):
    id_usuario = current_user.get_id()
    usuarios_por_pag = Config.query.first().n_elements
    centro = HelpCenter.query.filter_by(id=id).first()
    if User.tiene_permiso(id_usuario, 1):
        turnos = Appointment.query.filter_by(center_id = centro.id).paginate(page, per_page=usuarios_por_pag)
        return render_template('admin/turnos.html', turnos=turnos, centro=centro)
    else:
        flash('No tienes permisos para realizar esa acción.', 'danger')
        return redirect(url_for('admin.index'))


@ admin_bp.route('centro/crear_turno', methods=['GET', 'POST'])
@ admin_bp.route('centro/<id>/crear_turno', methods=['GET', 'POST'])
@ login_required
def crear_turno(id=0):

    # Lista de Listas con Horarios Disponibles para hoy, mañana y pasado mañana .

    # Consultar Qué turnos ya fueron tomados para el dia de hoy, ma;ana y pasado.

    availability = [
        ['9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00',
            '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30'],
        ['9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00',
            '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30'],
        ['9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00',
            '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30'],
    ]

    # Recibo una fecha y un horario.

    #

    return render_template('admin/turno_edit.html', horarios=availability)


@ admin_bp.route('centro/<id>/turnos', methods=['GET', 'POST'])
@ login_required
def actualizar_turno(id):

    # IMPLEMENTAR

    return render_template('admin/turno_edit.html')


@ admin_bp.route('centro/<id>/turnos', methods=['GET', 'POST'])
@ login_required
def eliminar_turno(id):

    # IMPLEMENTAR

    return 'Borrado de Turno'


#  API ROUTES #


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
        except:

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

     


@ admin_bp.route('/centros/<centro_id>/turnos_disponibles/', methods=["GET"])
def api_centro_turnos(centro_id):

    # IMPLEMENTAR
    # URL DE BUSQUEDA:
    # /centros/<centro_id>/turnos_disponibles/?fecha=xx/xx/xx
    # La fecha viene en args. CAPTURAR CON request.args.get('fecha')...
    return 'response'


@ admin_bp.route('/centros/<centro_id>/reserva', methods=["POST"])
def api_centro_reserva(centro_id):

    # IMPLEMENTAR

    return 'response'


#  TESTING ROUTES #

# ... #
