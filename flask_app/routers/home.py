import random
from flask import (Blueprint,request,session,flash,redirect,url_for,render_template)
import requests
from flask_app.models.user import User

from flask_app.models.city import City
from flask_app.models.city import Weather
from pymongo import MongoClient
import datetime
import time

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["capitales"]
recherche = db["recherche"]
loc=db["localisation"]

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route('/')
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
            print("Capitale introuvable dans la base de données")
 
        db.choix.insert_one({'capitale_id': ville_id, 'capitale': ville_nom, 'traite': 0})
        time.sleep(4)
        weather_data_db = recherche.find_one(sort=[('date', -1)])
        weather_data = City(None,
                            weather_data_db.ville,
                            weather_data_db.temps ,
                            weather_data_db.vent ,
                            "date",
                            weather_data_db.temperature,
                            weather_data_db.humidite ,
                            weather_data_db.pression_atmospherique)
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

@home_blueprint.route('/prevision')
def previsions():
    city = request.args.get('city')
    api_key = "d7094c960654ec3baf58f5e3e311fcf4"
    api_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

    # Récupérer les données de l'API
    response = requests.get(api_url).json()

    # Initialiser la liste des prévisions pour les 5 prochains jours
    forecasts = []

    # Définir une variable pour aujourd'hui, à minuit
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Parcourir toutes les données de la réponse de l'API
    for data in response['list']:

        # Convertir la date et l'heure en objet datetime
        date_time = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')

        # Calculer la différence en jours entre la date actuelle et la date des données
        days_difference = (date_time - today).days

        # Si la différence est supérieure à 5, sortir de la boucle
        if days_difference > 4:
            break

        # Si la différence est de 0 à 4, ajouter les données à la liste des prévisions
        if days_difference >= 0:

            # Convertir la température de Kelvin à Celsius
            temperature = round(data['main']['temp'] - 273.15, 1)

            # Ajouter la date, l'heure et la température à la liste des prévisions
            forecasts.append({
                'date': date_time.strftime('%Y-%m-%d'),
                'time': date_time.strftime('%H:%M:%S'),
                'temperature': temperature
            })

    return render_template('previson.html', forecasts=forecasts)


@home_blueprint.route('/favori')
def favori():
    return render_template('favori.html')