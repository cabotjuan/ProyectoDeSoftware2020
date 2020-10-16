# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms import TextAreaField, IntegerField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from app.models.model import User


class RegistrationForm(FlaskForm):
    """
    Formulario para crear una nueva cuenta de Admin
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


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
    site_enabled = RadioField('Sitio público habilitado', coerce=int, choices=[(1,'Habilitado'),(0,'Deshabilitado')])
    submit = SubmitField('Guardar cambios')