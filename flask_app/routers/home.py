import random
from flask import (Blueprint,request,session,flash,redirect,url_for,render_template)

from flask_app.models.user import User

from flask_app.models.city import City
from flask_app.models.city import Weather

import datetime

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route('/')
def home():
    user = request.args['user']
    current_date = datetime.date.today()
    usertest = User(15,"mahdi","aze","aze@mail.com")
    return render_template("index.html" ,user=usertest, cities=[],date =current_date.strftime("%d/%m/%Y") , city = City(1,"ariana",Weather("cloudy",89),15,"13:05",15,12,12))

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