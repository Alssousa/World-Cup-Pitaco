from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from copadomundo.models import Usuario


class FormAddPartida(FlaskForm):
    grupo = SelectField('Grupo', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'H'), ('H', 'H')])
    selecao_casa = SelectField('Seleção Casa', choices=[])
    selecao_fora = SelectField('Seleção Fora', choices=[])
    data_partida = DateField('Data da Partida', validators=[DataRequired()])
    hora_partida = TimeField('Hora Partida', validators=[DataRequired()])
    btn_submit = SubmitField('Adicionar')
    
    
class FormDefinirResultado(FlaskForm):
    casa_gol = IntegerField('Selecão Casa', validators=[DataRequired()])
    fora_gol = IntegerField('Selecão Fora', validators=[DataRequired()])
    status = SelectField('Situação da Partida', choices=[('Em andamento', 'Em andamento'), ('Finalizada', 'Finalizada'), ('Cancelada', 'Cancelada')])
    btn_submit = SubmitField('Confirmar Alterações')
    

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