import random
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.secret_key = 'secretweather'
app.config['MONGODB_SETTINGS'] = {
    'db': 'weather_db',
    'host': 'mongodb://localhost/weather_db'
}

db = MongoEngine(app)

class City(db.Document):
    name = db.StringField(required=True)
    temperature = db.StringField()
    humidity = db.StringField()
    atmospheric_pressure = db.StringField()
    precipitations = db.StringField()

class User(db.Document):
    username = db.StringField(required=True)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    favorites = db.ListField(db.ReferenceField('City'))
    historic = db.ListField(db.ReferenceField('City'))

def create_user(username, email, password):
    user = User(username=username, email=email, password=password)
    user.save()
    return user

def get_user_by_username(username):
    user = User.objects(username=username).first()
    return user

def get_user_by_id(user_id):
    user = User.objects(id=user_id).first()
    return user

def update_user_favorites(user, city_name):
    if city_name not in user.favorites:
        user.favorites.append(city_name)
        user.save()

def update_user_historic(user, city_name):
    if city_name not in user.historic:
        user.historic.append(city_name)
        user.save()

def create_city(name, temperature, humidity, atmospheric_pressure, precipitations):
    city = City(name=name, temperature=temperature, humidity=humidity, 
                atmospheric_pressure=atmospheric_pressure, precipitations=precipitations)
    city.save()
    return city

def get_city_by_name(name):
    city = City.objects(name=name).first()
    return city

@app.route('/login', methods=['POST'])
def login():
    session.pop('user_id', None) 
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        flash('Please enter your username and password.')
        return redirect(url_for('login'))

    user = get_user_by_username(username)
    if user and user.password == password:
        session['user_id'] = str(user.id)
        return redirect(url_for('profile'))

    flash('Invalid username or password.')
    return redirect(url_for('login'))



@app.route('/signup', methods=['POST'])
def signup():
    username = request.body['username']
    password = request.body['password']
    email = request.body['email']
    confirm_password = request.body['confirm_password']


    if not username or not password:
        flash('Please enter your username and password.')
        return redirect(url_for('signup'))
    
    if password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('signup'))

    if get_user_by_username(username):
        flash('Username already exists.')
        return redirect(url_for('signup'))

    user = create_user(username, email, password)
    return redirect(url_for('profile'))



@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first.')
        return redirect(url_for('login'))

    user = get_user_by_id(user_id)
    if not user:
        flash('Invalid user ID.')
        return redirect(url_for('login'))
    return render_template('profile.html', username=user.username, id=user.id)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))