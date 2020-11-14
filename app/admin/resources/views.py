from flask import flash, redirect, session, render_template, url_for, Blueprint, request, jsonify, make_response
from app.models.model import User, Role, Permission, users_roles, Config, HelpCenter, Status, CenterType, Appointment, HelpCenterSchema, CenterTypeSchema, StatusSchema, AppointmentSchema, UserSchema
from app.extensions import db
from app.admin.resources.forms import LoginForm, RegistrationForm, ConfigForm, EditForm, AppointmentForm
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
    centros = HelpCenter.query.paginate(page, per_page=items_per_page)
    return render_template('admin/centros.html', centros=centros, search=search)


@admin_bp.route('listado_centros/status=<status>/', methods=['GET', 'POST'])
@admin_bp.route('listado_centros/status=<status>/<int:page>', methods=['GET', 'POST'])
@login_required
def centros_filtrar_estado(status, page=1):

    # IMPLEMENTAR

    return render_template('admin/centros.html')


@admin_bp.route('centro/<id>', methods=['GET', 'POST'])
@login_required
def ver_centro(id):
    # IMPLEMENTAR

    return render_template('admin/centro.html')


@admin_bp.route('centro/crear', methods=['GET', 'POST'])
@login_required
def crear_centro():

    # IMPLEMENTAR
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

    return render_template('admin/centro_edit.html', municipios=sorted(results))


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

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  CRUD TURNOS #
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@ admin_bp.route('turnos/', methods=['GET', 'POST'])
@ admin_bp.route('turnos/<int:page>', methods=['GET', 'POST'])
@ login_required
def turnos(page=1):

    return render_template('admin/turnos.html')


@ admin_bp.route('turnos/centro=<search>', methods=['GET', 'POST'])
@ login_required
def turnos_buscar_centro(search):

    return render_template('admin/turnos.html')


@ admin_bp.route('turnos/email=<search>', methods=['GET', 'POST'])
@ login_required
def turnos_buscar_email(search):

    # IMPLEMENTAR
    # Filtra todos los turnos con el email recibido

    return render_template('admin/turnos.html')


@ admin_bp.route('centro/<id>/turnos', methods=['GET', 'POST'])
@ login_required
def turnos_centro(id):

    # IMPLEMENTAR
    # Trae los turnos de un dia de un centro

    return render_template('admin/turnos.html')

@admin_bp.route('centro/<id>/turnos/crear', methods=['GET', 'POST'])
@login_required
def crear_turno(id):
    """
        CREATE
        Registar un nuevo turno
        ID 12 TURNO_NEW permisos
    """
    id_usuario = current_user.get_id()
    if User.tiene_permiso(id_usuario, 12):
        centro = HelpCenter.query.get(id)
        centro_nombre = centro.name_center
        form = AppointmentForm()

        #POST
        if form.validate_on_submit():
            appointment = Appointment(
                email=form.email.data,
                start_time=form.start_time.data,
                appointment_date=form.appointment_date.data)
            delta = datetime.timedelta(minutes=30)
            start = appointment.start_time
            appointment.end_time = (datetime.datetime.combine(datetime.date(1,1,1),start) + delta).time()
            # Me trae el turno del centro recibido, con esa fecha y esa hora de inicio 
            turnos_del_dia = Appointment.query.filter_by(center_id=id,appointment_date=appointment.appointment_date,start_time=appointment.start_time).first()
            if not turnos_del_dia:
                centro.appointments.append(appointment)
                db.session.commit()
            else:
                flash('Turno no disponible', 'danger')
                return render_template('admin/turno_create.html', form=form, center_name=centro_nombre, title='Centros de Ayuda GBA - Sacar turno')

            # redirecciona a pagina turnos del dia del centro
            # return redirect(url_for('admin.turnos_centro({})'.format(id)))
            flash('Turno creado exitosamente', 'success')
            return redirect(url_for('admin.index'))
        return render_template('admin/turno_create.html', form=form, center_name=centro_nombre, title='Centros de Ayuda GBA - Sacar turno')
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
            turno_edit.end_time = (datetime.datetime.combine(datetime.date(1,1,1),start) + delta).time()
            # Me trae el turno del centro recibido, con esa fecha y esa hora de inicio 
            turnos_del_dia = Appointment.query.filter_by(center_id=turno_edit.center_id,appointment_date=turno_edit.appointment_date,start_time=turno_edit.start_time)
            if turnos_del_dia.count() == 1:
                db.session.commit()
                # redirecciona al listado de usuarios
                flash('Los cambios se guardaron correctamente.', 'success')
                return redirect(url_for('admin.index'))
            else:
                flash('Turno no disponible', 'danger')
                return render_template('admin/turno_edit.html', form=form, center_name=centro_nombre, title='Centros de Ayuda GBA - Actualizar turno')
        return render_template('admin/turno_edit.html', form=form, center_name=centro_nombre, title='Centros de Ayuda GBA - Actualizar turno')
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
            flash('El turno no existe.','danger')
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

        users = HelpCenter.query.all()
        
        # Serializar a JSON los Centros de Ayuda #

        help_center_schema = HelpCenterSchema(many=True)
        output = help_center_schema.dump(users)
        
        # Crear una respuesta HTTP 200 OK con el JSON de Centros de Ayuda #
        
        res = make_response(jsonify(output), 200, {
            'Content-Type': 'application/json; charset=utf-8'})

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
                jsonify({"mensaje":"No se pudo cargar el centro de ayuda."}), 400)
    
    return res


@ admin_bp.route('/centros/<centro_id>', methods=["GET"])
def api_centro(centro_id):


    # IMPLEMENTAR

    return 'response'


@ admin_bp.route('/centros/<centro_id>/turnos_disponibles/', methods=["GET"])
def api_centro_turnos(centro_id):

    """
         API endpoint: /centros/<centro_id>/turnos_disponibles/?fecha=<fecha>

         Method GET:
             Este servicio permite obtener el listado de los turnos disponibles
             para UN centro de ayuda en un dia en particular

    """

    data = {}
    data['turnos'] = []
    delta = datetime.timedelta(minutes=30)
    # date toma el dia pasado, si no se pasa el argumento toma el dia de hoy
    fecha = request.args.get('fecha')
    if fecha:
        date = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    else:
        date = datetime.date.today()
    todos_los_turnos=[datetime.time(9),datetime.time(9,30),
                    datetime.time(10),datetime.time(10,30),
                    datetime.time(11),datetime.time(11,30),
                    datetime.time(12),datetime.time(12,30),
                    datetime.time(13),datetime.time(13,30),
                    datetime.time(14),datetime.time(14,30),
                    datetime.time(15),datetime.time(15,30)]
    # Filtro los turnos del dia del centro recibido
    turnos_del_dia = Appointment.query.filter_by(center_id=centro_id,appointment_date=date)
    for turno in turnos_del_dia:
        todos_los_turnos.remove(turno.start_time)
    for turno in todos_los_turnos:
        fin = (datetime.datetime.combine(datetime.date(1,1,1),turno) + delta).time()
        data['turnos'].append({
            'centro_id': int(centro_id),
            'hora_inicio': turno.strftime("%H:%M"),
            'hora_fin': fin.strftime("%H:%M"),
            'fecha': date.strftime('%Y-%m-%d')
        })
    a = json.dumps(data, sort_keys=False)
    # Crear una respuesta HTTP 200 OK con el JSON de Turnos del dia #
    
    res = make_response(a, 200, {
        'Content-Type': 'application/json; charset=utf-8'})
    
    return res


@ admin_bp.route('/centros/<centro_id>/reserva', methods=["POST"])
def api_centro_reserva(centro_id):

    # IMPLEMENTAR
    # API

    return 'response'


#  TESTING ROUTES #

# ... #
