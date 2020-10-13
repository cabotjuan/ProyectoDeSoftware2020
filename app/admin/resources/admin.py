from flask import flash, redirect, render_template, url_for
#from app.models.users import User
from app import db
from forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, logout_user
#from flask import Blueprint
# Blueprint Administracion
 
#admin_bp = Blueprint('admin', __name__)

#@admin_bp.route('/')
@login_required
def index():
    """
        Renderiza la pagina principal de la administracion.
    """

    return render_template('admin/index.html')


#@admin_bp.route('/register/', methods=['GET', 'POST'])
def register():
    """
        Registra un nuevo usuario con RegistrationForm. Redirige a vista Login.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            role_id=1234)
        # add employee to the database
        db.session.add(user)
        db.session.commit()
        flash('Ya te registraste! Ahora inicia sesion.')

        # redirect to the login page
        return redirect(url_for('admin.login'))

    # load registration template
    return render_template('admin/register.html', form=form, title='Centros de Ayuda GBA - Registro')


#@admin_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """
        AUTENTICA A UN USUARIO MEDIANTE LoginForm. Si es valido, redirige a Administracion. 
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log employee in
            login_user(user)

            # redirect to the dashboard page after login
            return redirect(url_for('admin.index'))

        # when login details are incorrect
        else:
            flash('Email o contrasena incorrecta')

    # load login template
    return render_template('admin/login.html', form=form, title='Centros de Ayuda GBA - Iniciar Sesion')


#@admin_bp.route('/logout/')
@login_required
def logout():
    """
        FINALIZA LA SESION DEL USUARIO Y REDIRECCIONA A VISTA LOGIN.
    """
    logout_user()
    flash('Has cerrado sesion.')

    # redirect to the login page
    return redirect(url_for('admin.login'))
