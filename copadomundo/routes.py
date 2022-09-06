from copadomundo import app, bcrypt, database
from flask import request, render_template, redirect, url_for
from copadomundo.models import Usuario


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/usuario/novaconta', methods=['POST'])
def add_usuario():
    username = request.form.get("username")
    email = request.form.get("email")
    senha = request.form.get("senha")

    if username and email and senha:
        if not Usuario.query.filter_by(email=email).first():
            user = Usuario(username=username, email=email, senha=senha)
            database.session.add(user)
            database.session.commit()
            return redirect(url_for('home'))

    return render_template('cadastro.html')

@app.route('/usuario/login', methods=['POST'])
def login():
    return render_template('login.html')


@app.route('/liga/ranking')
def ranking_usuarios():
    return render_template('ranking_usuario.html')


@app.route('/selecoes/partida/addpartida', methods=['POST'])
def add_partida():
    return render_template('add_partida.html')


@app.route('/selecoes/partida/todas', methods=['POST', 'GET'])
def all_partidas():
    return render_template('all_partidas.html')


@app.route('/selecoes/partidas/<id_partida>', methods=['POST'])
def definir_resultado(id_partida):
    return render_template('definir_resultado.html', )