from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class FormAddPartida(FlaskForm):
    selecao_casa = StringField('Seleção Casa', validators=[DataRequired()])
    selecao_fora = StringField('Seleção Fora', validators=[DataRequired()])
    data_partida = DateField('Data da Partida', validators=[DataRequired()])
    btn_submit = SubmitField('Adicionar')

