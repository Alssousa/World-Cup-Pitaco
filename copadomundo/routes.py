from copadomundo import app, bcrypt, database
from flask import request, render_template, redirect, url_for, flash, jsonify
from copadomundo.models import Usuario, Partida, Selecao, Palpite, Grupo
from copadomundo.form import FormAddPartida, FormCadastro, FormLogin, FormDefinirResultado
from flask_login import login_user, logout_user, current_user, login_required
from collections import OrderedDict
from datetime import datetime, date, timedelta


@app.route('/')
def home():
    partidas = Partida.query.order_by(Partida.data_partida).all()
    datas_partidas = []
    data_atual = datetime.now()
    for partida in partidas:
        datas_partidas.append(str(partida.data_partida.date()))
    datas_partidas = list(OrderedDict.fromkeys(datas_partidas))
    
    partida = Partida.query.get(4)
    horas_meia_noite = datetime(data_atual.year, data_atual.month, data_atual.day, 00, 00, 00)
    
    print(horas_meia_noite)

    
    return render_template('home.html', partidas=partidas, data_atual=data_atual, horas_meia_noite=horas_meia_noite, timedelta=timedelta, datas_partidas=datas_partidas, str=str)


@app.route('/usuario/novaconta', methods=['GET', 'POST'])
def add_usuario():
    formcad = FormCadastro()
    
    if formcad.validate_on_submit():
        username = formcad.username.data
        email = formcad.email.data
        senha = formcad.password.data

        if username and email and senha:
            if not Usuario.query.filter_by(email=email).first():
                user = Usuario(username=username, email=email, senha=senha)
                database.session.add(user)
                database.session.commit()
                flash(f'Conta {user.username} criada com sucesso', 'alert-success')
                return redirect(url_for('home'))
            else:
                print("Email já esta em uso!")
                return redirect(url_for('add_usuario'))

    return render_template('tela_cad.html', formcad=formcad)


@app.route('/usuario/login', methods=['GET', 'POST'])
def login():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        email = formlogin.email.data
        password = formlogin.password.data
        if email and password:
            user = Usuario.query.filter_by(email=email, senha=password).first()
            if user:
                print("Login successful!")
                flash(f'Seja bem vindo {user.username}', 'alert-success')
                login_user(user)
                return redirect(url_for('home'))
            else:
                print("Login failed!")
                flash(f'Email ou senha incorreto.', 'alert-danger')
                return redirect(url_for('login'))
    return render_template('tela_login.html', formlogin=formlogin)



@app.route('/liga/ranking')
def ranking_usuarios():
    return render_template('ranking_usuario.html')


@app.route('/selecoes/partida/addpartida', methods=['GET', 'POST'])
@login_required
def add_partida():
    formaddpartida = FormAddPartida()
    formaddpartida.selecao_casa.choices = [(selecao.id, selecao.nome) for selecao in Selecao.query.filter_by(id_grupo=1).all()]
    formaddpartida.selecao_fora.choices = [(selecao.id, selecao.nome) for selecao in Selecao.query.filter_by(id_grupo=1).all()]
       
    if formaddpartida.is_submitted():
        print("\nENTROU AKIIIIIIIIIIIII\n")
        selecao_casa = Selecao.query.get(formaddpartida.selecao_casa.data)
        selecao_fora = Selecao.query.get(formaddpartida.selecao_fora.data)
        data_partida = formaddpartida.data_partida.data
        hora_partida = formaddpartida.hora_partida.data
        descricao = f"{selecao_casa.nome} x {selecao_fora.nome}"
        data = datetime(data_partida.year, data_partida.month, data_partida.day, hora_partida.hour, hora_partida.minute, 0)
        partida = Partida(descricao=descricao, data_partida=data)
        
        if selecao_casa.nome != selecao_fora.nome:
            if not Partida.query.filter_by(descricao=descricao).filter_by(data_partida=data_partida).first():
                try:
                    database.session.add(partida)
                    database.session.commit()
                except Exception as e:
                    print("Erro ao criar a partida: " + str(e))
                
                if selecao_casa and selecao_fora:
                    partida = Partida.query.filter_by(descricao=descricao).first()
                    print(f"\n{partida}\n")
                    selecao_casa.partidas.append(partida)
                    selecao_fora.partidas.append(partida)   
                    selecao_casa.qnt_jogos += 1   
                    selecao_fora.qnt_jogos += 1 
                    database.session.add_all([selecao_casa, selecao_fora])
                    database.session.commit()
                    print("\n\nPartida vinculada as selecoes")
        else:
            flash('Não pode adicionar uma partida onde as selecao casa e fora são as mesmas.', 'alert-danger')
        
        return redirect(url_for('add_partida'))
    
    return render_template('add_partida.html', formaddpartida=formaddpartida)


#Retorna um json com todas as selecoes do grupo referente ao parametro passado.
@app.route('/selecoes/<grupo>', methods=['GET', 'POST'])
def selecoes(grupo):
    grupo = Grupo.query.filter_by(nome_grupo=grupo).first()
    selecoes = Selecao.query.filter_by(id_grupo=grupo.id).all()
    
    selecoesArray = []
    
    for selecao in selecoes:
        selecaoObj = {}
        selecaoObj['id'] = selecao.id
        selecaoObj['name'] = selecao.nome
        selecoesArray.append(selecaoObj)
        
    return jsonify({'selecoes': selecoesArray})


@app.route('/selecoes/partida/todas', methods=['POST', 'GET'])
def todas_partidas():
    partidas = Partida.query.filter(Partida.status.not_like('Finalizada')).order_by(Partida.data_partida).all()
    datas_partidas = []
    data_atual = datetime.now()           
    
    if partidas:
        for partida in partidas:
            if partida.data_partida.date() not in datas_partidas:
                datas_partidas.append(partida.data_partida.date())

        print(datas_partidas)

    return render_template('partidas.html', partidas=partidas, datas_partidas=datas_partidas, data_atual=data_atual)


@app.route('/selecoes/partida/<id_partida>', methods=['GET', 'POST'])
def definir_resultado(id_partida):
    formresultado = FormDefinirResultado()
    partida = Partida.query.get(id_partida)
    partida.status = formresultado.status.data
    partida.gol_casa = formresultado.casa_gol.data
    partida.gol_fora = formresultado.fora_gol.data
    selecao_casa = Selecao.query.get(partida.selecoes[0].id)
    selecao_fora = Selecao.query.get(partida.selecoes[1].id)
    
    print(f"selecao casa: {selecao_casa.nome}, selecao fora: {selecao_fora.nome}")
    if formresultado.validate_on_submit():
        casa_gol = formresultado.casa_gol.data
        fora_gol = formresultado.fora_gol.data
        status = formresultado.status.data
        
        selecao_casa.gols_marcado = casa_gol
        selecao_fora.gols_marcado = fora_gol
        selecao_casa.gols_sofrido += fora_gol
        selecao_fora.gols_sofrido += casa_gol
        
        if casa_gol > fora_gol:
            selecao_casa.vitorias += 1
            selecao_casa.pontos += 3           
            selecao_fora.derrotas += 1          
        elif fora_gol > casa_gol:
            selecao_fora.vitorias += 1
            selecao_fora.pontos += 3           
            selecao_casa.derrotas += 1
        else:
            selecao_casa.pontos += 1
            selecao_fora.pontos += 1           
            selecao_fora.empates += 1
            selecao_casa.empates += 1
                   
        try:
            print("akiiii")
            database.session.add_all([selecao_casa, selecao_fora, partida])
            database.session.commit()
            flash('Resultado definido com sucesso', 'alert-success')
            return redirect(url_for('todas_partidas'))
        except Exception as e:
            print("Erro ao definir resultado da partida: " + str(e))
    
    return render_template('tela_add_resultado.html', formresultado=formresultado, selecao_casa=selecao_casa, selecao_fora=selecao_fora)


@app.route('/usuario/<partida>/palpite', methods=['GET', 'POST'])
@login_required
def palpite(partida):
    
    return render_template('home.html') 


@app.route('/selecao/grupos', methods=['GET', 'POST'])
def fase_grupos():
    selecoes = Selecao.query.order_by(Selecao.pontos.desc()).all()
    grupos = Grupo.query.all()
    
    
    return render_template('tela_grupos.html', selecoes=selecoes, grupos=grupos, enumerate=enumerate)


@app.route('/usuarios/ranking')
def ranking():
    usuarios = Usuario.query.all()
    
    return render_template('tela_rank.html', usuarios=usuarios)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso', 'alert-success')
    return redirect(url_for('home'))