from copadomundo import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    foto_user = database.Column(database.String, default='default.png')
    score = database.Column(database.Integer, default=0)
    acertos = database.Column(database.Integer, default=0)
    erros = database.Column(database.Integer, default=0)
    admin = database.Column(database.String, default=False)
    comentarios = database.relationship('Comentario', backref='usuario', lazy=True)
    

partida_selecao = database.Table('partidas',
    database.Column('selecao_id', database.Integer, database.ForeignKey('selecao.id'), primary_key=True),
    database.Column('partida_id', database.Integer, database.ForeignKey('partida.id'), primary_key=True)
)


class Comentario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data_criacao =  database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    corpo = database.Column(database.String, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)


class Selecao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_grupo = database.Column(database.Integer, database.ForeignKey('grupo.id'), nullable=False)
    id_eliminatoria = database.Column(database.Integer, database.ForeignKey('eliminatoria.id'))
    nome = database.Column(database.String, nullable=False, unique=True)
    foto_selecao = database.Column(database.String, default='selecao_default.png')
    pontos = database.Column(database.Integer, default=0)
    gols_marcado = database.Column(database.Integer, default=0)
    gols_sofrido = database.Column(database.Integer, default=0)
    vitorias = database.Column(database.Integer, default=0)
    derrotas = database.Column(database.Integer, default=0)
    empates = database.Column(database.Integer, default=0)
    qnt_jogos = database.Column(database.Integer, default=0)
    partidas = database.relationship('Partida', secondary=partida_selecao, lazy='subquery', backref=database.backref('selecoes', lazy=True))
        
    
    def add_selecoes(self):
        selecoes = ['Países Baixos', 'Equador', 'Senegal', 'Catar', 'Inglaterra', 'EUA', 'Irã', 'País de Gales',
                    'Polônia', 'Argentina', 'México', 'Arábia Saudita', 'França', 'Dinamarca', 'Tunísia', 'Austrália', 'Alemanha',
                    'Espanha', 'Costa Rica', 'Japão', 'Croácia', 'Bélgica', 'Canadá', 'Marrocos', 'Suíça', 'Sérvia', 'Brasil',
                    'Camarões', 'Portugal', 'Uruguai', 'Gana', 'Coreia do Sul']

        for i, selecao in enumerate(selecoes):
            if not Selecao.query.filter_by(nome=selecao).first():
                grupo_nome = ''
                if i < 4:
                    grupo_nome = 'A'
                elif i >= 4 and i < 8:
                    grupo_nome = 'B'
                elif i >= 8 and i < 12:
                    grupo_nome = 'C'
                elif i >= 12 and i < 16:
                    grupo_nome = 'D'
                elif i >= 16 and i < 20:
                    grupo_nome = 'E'
                elif i >= 20 and i < 24:
                    grupo_nome = 'F'
                elif i >= 24 and i < 28:
                    grupo_nome = 'G'
                elif i >= 28 and i < 32:
                    grupo_nome = 'H'

                try:
                    if not Grupo.query.filter_by(nome_grupo=grupo_nome).first():
                        grupo = Grupo(nome_grupo=grupo_nome)
                        database.session.add(grupo)
                        database.session.commit()

                    grupo = Grupo.query.filter_by(nome_grupo=grupo_nome).first()
                    time = Selecao(nome=selecao, foto_selecao=f"{selecao}.png", grupo=grupo)
                    database.session.add(time)
                    database.session.commit()
                except Exception as e:
                    print('Erro ao add as selecoes: ', e)
            


class Partida(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    descricao = database.Column(database.String, nullable=False)
    gol_casa = database.Column(database.Integer, default=0)
    gol_fora = database.Column(database.Integer, default=0)
    data_partida = database.Column(database.DateTime, default=datetime.now())
    palpites = database.relationship('Palpite', backref='partida', lazy=True)
    status = database.Column(database.String, default="aguardando")

class Grupo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_grupo = database.Column(database.String, nullable=False, unique=True)
    selecoes = database.relationship('Selecao', backref='grupo', lazy=True)
    
    
class Eliminatoria(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    etapa = database.Column(database.String, nullable=False, unique=True)
    selecoes = database.relationship('Selecao', backref='fase', lazy=True)
    status = database.Column(database.String, default="aguardando")


class Palpite(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_partida = database.Column(database.Integer, database.ForeignKey('partida.id'), nullable=False)
    palpite = database.Column(database.String, nullable=False)
    status = database.Column(database.String, default="Aguardando")
    












