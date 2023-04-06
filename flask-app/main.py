
import random
from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Blueprint
)

class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='admin', password='admin',email=''))
'''
users.append(User(id=1, username='wassim', password='8888'))
users.append(User(id=3, username='sarra', password='1234'))
users.append(User(id=2, username='mahdi', password='0000'))
'''


app = Flask(__name__)
app.secret_key = 'secretweather'




countries = [{
    'country' : "tunisie",
    'lat' : "",
    'lon' :""
    }]
cities = [{
    'city' : "ariana",
    'lat' : "36.862499",
    'lon' :"10.195556",
    'weather' :"cloudy"
    },
    {
    'city' : "tunis",
    'lat' : "33.886917",
    'lon' :"9.537499",
    'weather':"sunny"
    }]




@app.route("/")
def index():
    redirect(url_for('login'))

@app.route('/<string:cityname>')
def displayCityDetail(cityname):
    
    searchedcity = ""
    for city in cities:
        if( cityname== city['city']):
            searchedcity = city 
    return render_template("index.html" , cities=cities, city = searchedcity)


@app.route('/map')
def map():
    countries = [{
        'country' : "tunisie",
        'lat' : "",
        'lon' :""
    }]
    cities = [{
        'city' : "ariana",
        'lat' : "36.862499",
        'lon' :"10.195556"
    },
    {
        'city' : "tunis",
        'lat' : "33.886917",
        'lon' :"9.537499"
    }]
    return render_template("map.html", data= {'countries':countries , 'cities' : cities})

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/favori')
def favori():
    return render_template('favori.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please enter your username and password.')
            return redirect(url_for('login'))

        user = [x for x in users if x.username == username]
        if user and user[0].password == password:
            session['user_id'] = user[0].id
            return redirect(url_for('home'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')
    
@app.route('/signup', methods=['POST'])
def signup_post():
    
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    if not username or not password:
        flash('Please enter your username and password.')
        return redirect(url_for('signup'))

    if any(user.username == username for user in users):
        flash('Username already exists.')
        return redirect(url_for('signup'))

    user = User(id=random.randint(2,100), username=username, password=password, email=email)
    users.append(user)

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first.')
        return redirect(url_for('login'))

    user = next((user for user in users if user.id == user_id), None)
    if not user:
        flash('Invalid user ID.')
        return redirect(url_for('login'))

    return render_template('profile.html', username=user.username, id=user.id)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)