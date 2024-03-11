from flask import Flask, render_template, redirect, request, url_for, flash, session
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Agenda777"
)

cursor = db.cursor()

def encripcontra(contraencrip):
    # generar un hash de la contraseña
    encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'), bcrypt.gensalt())
    return encriptar 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #VERIFICAR LAS CREDENCIALES DEL USUARIO
        username = request.form.get('txtusuario')
        password = request.form.get('txtcontrasena')

        cursor.execute('SELECT usuarioper,contraper FROM personas where usuarioper = %s', (username,))
        usuario = cursor.fetchone()
        
        if usuario and bcrypt.check_password_hash(usuario[1], password):
            session['usuario'] = username
            return redirect(url_for('lista'))
        else:
            flash('Credenciales inválidas, por favor inténtalo de nuevo', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/')
def lista():
    if 'usuario' in session:
        cursor.execute('SELECT * FROM personas')
        personas = cursor.fetchall()
        return render_template('index.html', personas=personas)
    else:
        return redirect(url_for('login'))

@app.route('/Registrar', methods=['GET', 'POST'])
def Registrar_usuario():
    if request.method == 'POST':
        Nombres = request.form.get('nombre')
        Apellidos = request.form.get('apellido')
        Email = request.form.get('email')
        Direccion = request.form.get('direccion')
        Telefono = request.form.get('telefono')
        Usuario = request.form.get('usuario')
        Contrasena = request.form.get('contrasena')

        Contrasenaencriptada = encripcontra(Contrasena)

        cursor.execute("SELECT * FROM personas WHERE usuarioper = %s", (Usuario,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Usuario ya existe', 'error')
            return redirect(url_for('Registrar_usuario'))

        cursor.execute("INSERT INTO personas(nombreper, apellidoper, emailper, dirper, telper, usuarioper, contraper) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Contrasenaencriptada))
        db.commit()
        flash('Usuario creado correctamente', 'success')

        return redirect(url_for('Registrar_usuario'))
    return render_template('Registrar.html')

@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar_usuario(id):
    if request.method == 'POST':
        nombreper = request.form.get('nombreper')
        apellidoper = request.form.get('apellidoper')
        emailper = request.form.get('emailper')
        dirper = request.form.get('direccionper')
        telper = request.form.get('telefonoper')
        usuarioper = request.form.get('usuarioper')
        passper = request.form.get('passwordper')

        sql = "UPDATE personas SET nombreper=%s, apellidoper=%s, emailper=%s, dirper=%s, telper=%s, usuarioper=%s, contraper=%s WHERE idper=%s"
        cursor.execute(sql, (nombreper, apellidoper, emailper, dirper, telper, usuarioper, passper, id))
        db.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('lista'))
    else:
        cursor.execute('SELECT * FROM personas WHERE idper = %s', (id,))
        data = cursor.fetchone()
        if data:
            return render_template('Editar.html', personas=data)
        else:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('lista'))

@app.route('/eliminar/<int:id>', methods=['POST', 'DELETE'])
def eliminar_usuario(id):
    if request.method == 'POST' or request.method == 'DELETE':
        cursor.execute('DELETE FROM Personas WHERE idper = %s', (id,))
        db.commit()
        flash('Usuario eliminado correctamente', 'success') 
        return redirect(url_for('lista'))

if __name__ == '__main__':
    app.run(debug=True, port=5005)

