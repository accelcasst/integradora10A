from flask import Flask, render_template, request, redirect, url_for, flash
from config import config

from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from models import ModelPrice

#Models
from models.ModelUser import ModelUser
from models.ModelVehiculo import ModelVehiculo
from models.ModelParking import ModelParking
from models.ModelPrice import ModelPrice

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
                    return render_template()
                else:
                    return redirect(url_for('menu_vehiculos'))
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

@app.route('/sign_up')
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
                #Mandar allamar ese metodo y se guardara en una variable como la lista de usuarios y se pasa al 
                #formulario de add_vehiculo.html para que dentro se itere y se construyan las opciones de estacionamiento.
                return redirect(url_for('get_list_full'))
            else:
                flash("Invalid password...")
            return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
        

@app.route('/lista_users/edit/<id>')
@login_required
def get_user(id):
    return render_template('edit_user.html', user = ModelUser.get_user(db, id))

@app.route('/lista_users/update/<id>', methods = ['POST'])
@login_required
def update_user(id):
    if request.method == 'POST':
        user_id = request.view_args['id']

        ModelUser.update_user(db,request.form['fullname'],request.form['email']
                              ,request.form['username'],request.form['password'], user_id)
        flash('Usuario actualizado')
        return redirect(url_for('get_list_full'))
    
@app.route('/lista_users/delete/<string:id>')
@login_required
def delete_user(id):
   ModelUser.delete_user(db,id)
   flash('Usuario eliminado correctamente',)
   return redirect(url_for('get_list_full'))

@app.route('/menu_vehiculos')
@login_required
def menu_vehiculos():
   return render_template('menu_vehiculo.html')

@app.route('/input_vehiculos')
@login_required
def input_vehiculos():
   return render_template('add_vehiculo.html')

@app.route('/add_vehiculo',methods = ['POST'])
@login_required
def add_vehiculo():
    if request.method == 'POST':
        vehiculo = ModelVehiculo.add_vehiculo(db,dati.now(),request.form['plate'], int(request.form['parking_id']))
        print(vehiculo)
        if vehiculo != None:
            if vehiculo.id == "LLENO":
                flash('Estacionamiento llenó')
                return render_template('add_vehiculo.html')
            if vehiculo.id == "ERROR":
                flash('Vehiculo registrado en otro estacionamiento')
                return render_template('add_vehiculo.html')
            else:
                flash('Vehiculo agregado correctamente')
                return render_template('add_vehiculo.html')
        else:
            flash('El vehiculo se encuentra estacionado')
            return render_template('add_vehiculo.html')

@app.route('/get_full_vehiculos')
@login_required
def get_full_vehiculos():
   return render_template('get_vehiculos.html', listt_vehiculos = ModelVehiculo.get_full_vehiculos(db))

@app.route('/add_parking', methods=['GET','POST'])
@login_required
def add_parking():
    if request.method == 'POST':
        print(request.form['parking_name'])
        print(request.form['space'])
        parking = ModelParking.add_parking(db,request.form['parking_name'], 
                                           request.form['location'],request.form['phone_number'],(request.form['space']))
        if parking != None:
            flash('Estacionamiento agregado correctamente')
            return render_template('add_parking.html')
        else:
            flash('El Estacionamiento se encuentra registrado')
            return render_template('add_parking.html')
        
@app.route('/lista_parkings/edit/<id>')
@login_required
def update_parking(id):
    return render_template('edit_parkings.html', parkings = ModelParking.get_parking(db, id))
        
@app.route('/lista_parkings/update/<id>', methods = ['POST'])
@login_required
def update_parkings(id):
    if request.method == 'POST':
        parking_id = request.view_args['id']

        ModelParking.update_parking(db,request.form['parking_name'],request.form['location']
                                     ,request.form['phone_number'],request.form['space'], parking_id)
        flash('Estacionamiento actualizado')
        return render_template('get_parkings.html', listt_parkings = ModelParking.get_full_parking(db))

@app.route('/lista_parkings/delete/<string:id>')
@login_required
def delete_parking(id):
   ModelParking.delete_parking(db,id)
   flash('Usuario eliminado correctamente',)
   return render_template('get_parkings.html', listt_parkings = ModelParking.get_full_parking(db))

@app.route('/register_parking')
def render_parking():
    return render_template('add_parking.html')

@app.route('/get_full_parkings')
def get_full_parkings():
    return render_template('get_parkings.html', listt_parkings = ModelParking.get_full_parking(db))

@app.route('/add_prices', methods=['GET','POST'])
@login_required
def add_price():
    if request.method == 'POST':
        print(request.form['parking_id'])
        print(request.form['tolerance_time'])
        price = ModelPrice.add_price(db,request.form['time_min'], 
                                           request.form['time_max'],request.form['tolerance_time'],(request.form['payment']),(request.form['parking_id']))
        if price != None:
            flash('Precio registrado correctamente')
            return render_template('add_parking.html')
        else:
            flash('El precio ya se encuentra registrado')
            return render_template('add_prices.html')
        
@app.route('/register_prices')
def register_prices():
    return render_template('add_prices2.html')

@app.route('/get_prices')
def get_prices():
    return render_template('get_prices.html')

@app.route('/paid_bill')
def paid_ball():
    return render_template('paid_bill.html')

@app.route('/ver_pagos')
def ver_pagos():
    return render_template('ver_pagos.html')

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
