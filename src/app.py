from flask import Flask, render_template, request, redirect, url_for, flash
from config import config

from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

#Models
from models.ModelUser import ModelUser
from models.ModelVehiculo import ModelVehiculo
from models.ModelParking import ModelParking

#Entities
from models.entities.User import User
from models.entities.Vehiculo import Vehiculo
from models.entities.Parking import Parking

#DATETIME
from datetime import datetime as dati

app = Flask(__name__)

csrf=CSRFProtect()

db=MySQL(app)

login_manager_app=LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        user = User(0,request.form['username'],request.form['password'])
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                if(logged_user.rol == "SUPER-ADMIN"):
                    return redirect(url_for('get_list_full'))
                elif (logged_user.rol == "ADMIN"):
                    return redirect(url_for('get_list_users'))
                else:
                    return render_template('add_vehiculo.html')
            else:
                flash("Invalid password...")
            return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/get_list_full')
def get_list_full():
    return render_template('get_users.html', listt_users = ModelUser.get_full_users(db), rol = 'SUPER-ADMIN')


@app.route('/get_list_users')
def get_list_users():
    return render_template('get_users.html', listt_users = ModelUser.get_list_users(db), rol = 'ADMIN')

@app.route('/sing_up')
def sign_up():
    return render_template('add_user.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ModelUser.add_user(db,request.form['fullname'],request.form['email'],username, password)
        flash('Usuario agregado correctamente')
        
        user = User(0,username, password)
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return render_template('add_vehiculo.html')
            else:
                flash("Invalid password...")
            return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
        

@app.route('/lista_users/edit/<id>')
@login_required
def get_user(id):
    return render_template('edit_user.html', user = ModelUser.get_user(id))

@app.route('/lista_users/update/<id>', methods = ['POST'])
@login_required
def update_user(id):
    if request.method == 'POST':
        ModelUser.update_user(db,request.form['fullname'],request.form['email']
                              ,request.form['username'],request.form['password'], id)
        flash('Usuario actualizado')
        return redirect(url_for('get_list_full'))
    
@app.route('/lista_users/delete/<string:id>')
@login_required
def delete_user(id):
   ModelUser.delete_user(db,id)
   flash('Usuario eliminado correctamente',)
   return redirect(url_for('get_list_full'))

@app.route('/add_vehiculo',methods = ['POST'])
@login_required
def add_vehiculo():
    if request.method == 'POST':
        print(request.form['plate'])
        print(request.form['parking_id'])
        vehiculo = ModelVehiculo.add_vehiculo(db,dati.now(),request.form['plate'], int(request.form['parking_id']))
        if vehiculo != None:
            flash('Vehiculo agregado correctamente')
        else:
            flash('El vehiculo se encuentra estacionado')

@app.route('/add_parking', methods = ['POST'])
@login_required
def add_parking():
    if request.method == 'POST':
        print(request.form['parkings'])
        print(request.form['space'])
        parking = ModelParking.add_parking(db,dati.now(),request.form['parkings'], int(request.form['space']))
        if parking != None:
            flash('Estacionamiento agregado correctamente')
        else:
            flash('El Estacionamiento se encuentra registrado')

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>"

#Correr la aplicación
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run(debug=True, port=8000)
            #Modo depuración,permite realizar los cambios corriendo