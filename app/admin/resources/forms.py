# app/auth/forms.py

import datetime
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectMultipleField, TimeField
from wtforms import TextAreaField, IntegerField, BooleanField, RadioField, HiddenField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, NoneOf
from app.models.model import User, Role
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.widgets import html5 as widgets


class MultiCheckboxfield(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class UserForm(FlaskForm):
    """
    Formulario general del usuario
    """
    id = HiddenField('id')
    submit = SubmitField('Guardar')
    email = StringField('Email', validators=[
                        DataRequired('Este campo es requerido'), Email()])
    username = StringField('Nombre de Usuario', validators=[
                           DataRequired('Este campo es requerido')])
    first_name = StringField('Nombre', validators=[
                             DataRequired('Este campo es requerido')])
    last_name = StringField('Apellido', validators=[
                            DataRequired('Este campo es requerido')])
    admin = BooleanField('Administrador')
    operator = BooleanField('Operador')


class RegistrationForm(UserForm):
    """
    Formulario para crear una nueva cuenta de Usuario
    """
    active = BooleanField('Activo', render_kw={'checked': True})
    password = PasswordField('Contraseña', validators=[
        DataRequired('Este campo es requerido'),
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
    email = StringField('Email', validators=[
                        DataRequired('Este campo es requerido'), Email()])
    password = PasswordField('Contraseña', validators=[
                             DataRequired('Este campo es requerido')])
    submit = SubmitField('Iniciar sesión')


class ConfigForm (FlaskForm):
    """
    Formulario para configurar informacion de pagina
    """
    title = StringField('Título', validators=[DataRequired(
        'Este campo es requerido'), Length(max=40)])
    description = TextAreaField('Descripción', validators=[
                                DataRequired('Este campo es requerido')])
    email = StringField('Email', validators=[
                        DataRequired('Este campo es requerido'), Email()])
    n_elements = IntegerField('Numero de elementos', validators=[
                              DataRequired('Este campo es requerido'), NumberRange(min=0)])
    site_enabled = BooleanField('Sitio público habilitado')
    submit = SubmitField('Guardar cambios')


class HelpCenterForm (FlaskForm):
    """
    Formulario para Centros de ayuda
    """
    name_center = StringField('Nombre de centro', validators=[
                              DataRequired('Este campo es requerido'), Length(max=40)])
    address = StringField('Dirección', validators=[
                          DataRequired('Este campo es requerido'), Length(max=60)])
    phone = IntegerField('Teléfono', validators=[
                         DataRequired('Este campo es requerido')])
    opening_time = TimeField('Hora de apertura', validators=[DataRequired(
        'Este campo es requerido')], format='%H:%M', widget=widgets.TimeInput())
    close_time = TimeField('Hora de cierre', validators=[DataRequired(
        'Este campo es requerido')], format='%H:%M', widget=widgets.TimeInput())
    town = SelectField('Municipio', validators=[
                       DataRequired('Este campo es requerido')])
    web = StringField('Página web')
    email = StringField('Email', validators=[Optional(), Email()])
    visit_protocol = FileField('Protocolo de visita', validators=[
                               Optional(), FileAllowed(['pdf'], 'Solo archivos pdf')])
    center_type_id = SelectField('Tipo de centro', validators=[
                                 DataRequired('Este campo es requerido')])
    latitude = StringField('Latitud', validators=[
                           DataRequired('Este campo es requerido')])
    longitude = StringField('Longitud', validators=[
                            DataRequired('Este campo es requerido')])
    submit = SubmitField('Guardar cambios')


class AppointmentForm(FlaskForm):
    """
    Formulario general de turnos
    """
    id = HiddenField('id')
    submit = SubmitField('Guardar')
    email = StringField('Email', validators=[
                        DataRequired('Este campo es requerido'), Email()])
    first_name = StringField('Nombre', validators=[
        DataRequired('Este campo es requerido')])
    last_name = StringField('Apellido', validators=[
        DataRequired('Este campo es requerido')])
    phone = IntegerField('Telefono', validators=[
        DataRequired('Este campo es requerido')])
    start_time = TimeField('Hora de inicio:', validators=[DataRequired(
        'Este campo es requerido')], format='%H:%M')
    appointment_date = DateField('Fecha:', validators=[DataRequired(
        'Este campo es requerido')], format='%Y-%m-%d')

    def validate_start_time(self, field):
        if field.data < datetime.time(9):
            raise ValidationError('Los turnos se dan desde las 9:00.')
        if field.data > datetime.time(15, 30):
            raise ValidationError('Los turnos se dan hasta las 15:30.')

    def validate_appointment_date(self, field):
        if field.data < datetime.date.today():
            raise ValidationError('La fecha debe ser desde el dia de hoy.')


class AppointmentWithCenterForm(AppointmentForm):
    """
    Formulario de turnos con selector de centro de ayuda
    """
    center_id = SelectField('Centro de ayuda', validators=[
                            DataRequired('Este campo es requerido')])
