from copadomundo import app, bcrypt, database
from flask import request, render_template, redirect, url_for
from copadomundo.models import Usuario, Partida, Selecao, Palpite
from copadomundo.form import FormAddPartida, FormCadastro, FormLogin


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/usuario/novaconta', methods=['GET', 'POST'])
def add_usuario():
    formcadastro = FormCadastro()
    username = formcadastro.username.data
    email = formcadastro.email.data
    senha = formcadastro.password.data

    if username and email and senha:
        if not Usuario.query.filter_by(email=email).first():
            user = Usuario(username=username, email=email, senha=senha)
            database.session.add(user)
            database.session.commit()
            return redirect(url_for('home'))
    else:
        print("Email já esta em uso!")
        return redirect(url_for('add_usuario'))

    return render_template('tela_cad.html')


@app.route('/usuario/login', methods=['GET', 'POST'])
def login():
    formlogin = FormLogin()
    email = formlogin.email.data
    password = formlogin.password.data
    if email and password:
        if Usuario.quert.filter_by(email=email, password=password).first():
            print("Login successful!")
            return redirect(url_for('home'))
        else:
            print("Login failed!")
            return redirect(url_for('login'))
    return render_template('tela_login.html')



@app.route('/liga/ranking')
def ranking_usuarios():
    return render_template('ranking_usuario.html')


@app.route('/selecoes/partida/addpartida', methods=['GET', 'POST'])
def add_partida():
    formaddpartida = FormAddPartida()
    
    if formaddpartida.validate_on_submit():
        selecao_casa = formaddpartida.selecao_casa.data
        selecao_fora = formaddpartida.selecao_fora.data
        data_partida = formaddpartida.data_partida.data
        descricao = f"{selecao_casa} x {selecao_fora}"
        partida = Partida(descricao=descricao, data_partida=data_partida)
        
        if not Partida.query.filter_by(descricao=descricao).filter_by(data_partida=data_partida).first():
            try:
                database.session.add(partida)
                database.session.commit()
            except Exception as e:
                print("Erro ao criar a partida: " + str(e))
                
            selecao_casa = Selecao.query.filter_by(nome=selecao_casa).first()
            selecao_fora = Selecao.query.filter_by(nome=selecao_fora).first()
            
            if selecao_casa and selecao_fora:
                partida = Partida.query.filter_by(descricao=descricao).first()
                print(f"\n{partida}\n")
                selecao_casa.partidas.append(partida)
                selecao_fora.partidas.append(partida)       
                database.session.add_all([selecao_casa, selecao_fora])
                database.session.commit()
                print("\n\nPartida vinculada as selecoes")
        
        return redirect(url_for('add_partida'))
    
    return render_template('add_partida.html', formaddpartida=formaddpartida)


@app.route('/selecoes/partida/todas', methods=['POST', 'GET'])
def all_partidas():
    return render_template('all_partidas.html')


@app.route('/selecoes/partidas/<id_partida>', methods=['POST'])
def definir_resultado(id_partida):
    return render_template('definir_resultado.html', )