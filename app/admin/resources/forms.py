# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectMultipleField
from wtforms import TextAreaField, IntegerField, BooleanField, RadioField, HiddenField, SelectField, TimeField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from app.models.model import User, Role
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.widgets import html5 as widgets
import datetime

class MultiCheckboxfield(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class UserForm(FlaskForm):
    """
    Formulario general del usuario
    """
    id = HiddenField('id')
    submit = SubmitField('Guardar')
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    admin = BooleanField('Administrador')
    operator = BooleanField('Operador')

class RegistrationForm(UserForm):
    """
    Formulario para crear una nueva cuenta de Usuario
    """
    active = BooleanField('Activo', render_kw={'checked': True})
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirmar Contraseña')
    submit = SubmitField('Guardar')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('El mail ya existe.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('El nombre de usuario ya existe.')

class EditForm(UserForm):
    """
    Formulario para editar una cuenta de Usuario
    """
    def validate_email(self, field):
        existing_user = User.query.filter_by(email=field.data).first()
        if existing_user:
            if self.id == existing_user.id:
                raise ValidationError('El mail ya existe.')

    def validate_username(self, field):
        existing_user = User.query.filter_by(username=field.data).first()
        if existing_user:
            if self.id == existing_user.id:
                raise ValidationError('El nombre de usuario ya existe.')

class LoginForm(FlaskForm):
    """
    Formulario para autenticarse
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class ConfigForm (FlaskForm):
    """
    Formulario para configurar informacion de pagina
    """
    title = StringField('Título', validators=[DataRequired(), Length(max=40)])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    n_elements = IntegerField('Numero de elementos', validators=[DataRequired(), NumberRange(min=0)])
    site_enabled = BooleanField('Sitio público habilitado')
    submit = SubmitField('Guardar cambios')

class AppointmentForm(FlaskForm):
    """
    Formulario general de turnos
    """
    id = HiddenField('id')
    submit = SubmitField('Guardar')
    email = StringField('Email', validators=[DataRequired(), Email()])
    start_time = TimeField('Hora de inicio:', validators=[DataRequired()],format='%H:%M', widget = widgets.TimeInput())
    appointment_date = DateField('Fecha:', validators=[DataRequired()], format='%Y-%m-%d')

    def validate_start_time(self, field):
        if field.data < datetime.time(9):
            raise ValidationError('Los turnos se dan desde las 9:00.')
        if field.data > datetime.time(15,30):
            raise ValidationError('Los turnos se dan hasta las 15:30.')

    def validate_appointment_date(self, field):
        if field.data < datetime.date.today():
            raise ValidationError('La fecha debe ser desde el dia de hoy.')