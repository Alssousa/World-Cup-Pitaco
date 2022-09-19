from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from copadomundo.models import Usuario


class FormAddPartida(FlaskForm):
    selecao_casa = StringField('Seleção Casa', validators=[DataRequired()])
    selecao_fora = StringField('Seleção Fora', validators=[DataRequired()])
    data_partida = DateField('Data da Partida', validators=[DataRequired()])
    hora_partida = TimeField('Hora Partida', validators=[DataRequired()])
    btn_submit = SubmitField('Adicionar')


class FormCadastro(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    btn_submit = SubmitField('Cadastrar')
    
    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('O email já esta em uso. Favor, tente outro email ou faça login para continuar')
    
    
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    btn_submit = SubmitField('Login')