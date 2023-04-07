import random
from flask import (
    Flask,
    jsonify,
    request,
    session,
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
    data = request.get_json()
    session.pop('user_id', None)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Please enter your username and password.'})

    user = get_user_by_username(username)
    if user and user.password == password:
        session['user_id'] = str(user.id)
        return jsonify({'message': 'Login successful.', 'user_id': str(user.id)})

    return jsonify({'error': 'Invalid username or password.'})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    confirm_password = data.get('confirm_password')

    if not username or not password:
        return jsonify({'error': 'Please enter your username and password.'})
    
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'})

    if get_user_by_username(username):
        return jsonify({'error': 'Username already exists.'})

    user = create_user(username, email, password)
    return jsonify({'message': 'User created successfully.', 'user_id': str(user.id)})

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Please login first.'}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'Invalid user ID.'}), 401

    return jsonify({'username': user.username, 'id': str(user.id)})

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'You have been logged out.'})

if __name__ == '__main__':
    app.run(debug=True)