
import importlib
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

from flask_app.models.user import User
from flask_app.routers.authentication import authentication_blueprint
from flask_app.routers.home import home_blueprint

app = Flask(__name__)
app.secret_key = 'secretweather'

app.register_blueprint(authentication_blueprint,url_prefix='/auth')
app.register_blueprint(home_blueprint,url_prefix='/home')
print(app.url_map)








users = []
users.append(User(id=1, username='admin', password='admin',email=''))
'''
users.append(User(id=1, username='wassim', password='8888'))
users.append(User(id=3, username='sarra', password='1234'))
users.append(User(id=2, username='mahdi', password='0000'))
'''








@app.route("/")
def index():
    return redirect(url_for('authentication_blueprint.login'))

# @app.route('/<string:cityname>')
# def displayCityDetail(cityname):
    
#     searchedcity = ""
#     cities = []
#     for city in cities:
#         if( cityname== city['city']):
#             searchedcity = city 
#     return render_template("index.html" , cities=cities, city = searchedcity)


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











if __name__ == "__main__":
    app.run(debug=True)


