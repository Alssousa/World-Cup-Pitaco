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


