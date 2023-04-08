import random
from flask import (Blueprint,request,session,flash,redirect,url_for,render_template)

from flask_app.models.user import User

from flask_app.models.city import City
from flask_app.models.city import Weather

import datetime
import time
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["capitales"]
recherche = db["recherche"]
loc=db["localisation"]

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["capitales"]
recherche = db["recherche"]
loc=db["localisation"]

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route('/',methods=['GET','POST'])
def home():
    cities = db.capitales.find()
    print(cities)
    geol = loc.find_one()
    if request.method == 'POST':
        ville_nom = request.form['city']
        capitale = collection.find_one({"nom": ville_nom})
        if capitale:
            ville_id = capitale["_id"]
        else:
            weather_data = City(None,
                            geol['ville'],
                            geol['temps'] ,
                            geol['vent'] ,
                            "hj",
                            geol['temperature'],
                            geol['humidite'] ,
                            geol['pression_atmospherique'])
            return render_template("index.html", cities=cities, city=weather_data, message="La ville entrée n'est pas dans la base de données.")

        db.choix.insert_one({'capitale_id': ville_id, 'capitale': ville_nom, 'traite': 0})
            
 
        
        time.sleep(4)
        weather_data_db = recherche.find_one(sort=[('date', -1)])
        print(weather_data_db)
        
        weather_data = City(None,
                            weather_data_db['ville'],
                            weather_data_db['temps'] ,
                            weather_data_db['vent'] ,
                            weather_data_db['temperature'],
                            weather_data_db['humidite'] ,
                            weather_data_db['pression_atmospherique'])
        return render_template('index.html',cities=cities, city=weather_data)
        #return render_template("resultat.html", ville=ville_nom)
    

    # user = request.args['user']
    
    current_date = datetime.date.today()
    usertest = User(15,"mahdi","aze","aze@mail.com")
    usertest = None
    city = City(1,"ariana","cloudy",15,"13:05",15,12,12)
    
    return render_template("index.html" ,user=usertest, cities=cities,date =current_date.strftime("%d/%m/%Y") , city = City(1,"ariana","cloudy",15,"13:05",15,12,12))

@home_blueprint.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first.')
        return redirect(url_for('login'))

    user = User(15,"mahdi","aze","aze@mail.com")
    if not user:
        flash('Invalid user ID.')
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)




@home_blueprint.route('/favori')
def favori():
    return render_template('favori.html')
@home_blueprint.route('/historic')
def historic():
    return render_template('historique.html')