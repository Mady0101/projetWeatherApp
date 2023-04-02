import json
from confluent_kafka import Producer
import requests
import geocoder
import pymongo

def get_weatherdata(ville):
    # Remplacez {API key} par votre propre clé API
    api_key = "0747defefc71f82a572276d367a1be31"
    print("Li wsel",ville)
        # URL de l'API avec les paramètres de la ville et de la clé API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}"
            
    # Envoyer une requête GET à l'API
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Extraire les données JSON de la réponse
        data = response.json()

        # Convertir la température de Kelvin en Celsius
        temp_celsius = data['main']['temp'] - 273.15

        # Créer un dictionnaire pour stocker les données météorologiques
        weather_data = {
            'ville': ville,
            'temps': data['weather'][0]['description'],
            'temperature': temp_celsius,
            'pression_atmospherique': data['main']['pressure'],
            'humidite': data['main']['humidity']
        }

        # Convertir le dictionnaire en JSON
        weather_data_json = json.dumps(weather_data)
        print("Je vais essayer d'envoyer")
        print(weather_data)
       

        # Créer un producteur Kafka
        producer = Producer({'bootstrap.servers': 'broker:29092'})
        print("Je me suis connecté")
        producer.poll(1)
        # Envoyer les données météorologiques au sujet "weather" 
        producer.produce('weather2', weather_data_json)
        
        # Fermer le producteur Kafka
        producer.flush()
        
    else:
        # Afficher le code d'erreur HTTP si la requête a échoué
        print(f"Erreur de requête : {response.status_code}")

    print("Jai envoyé")


# Connexion à la base de données MongoDB
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
collection = db["choix"]



ville = collection.find_one({"traite": 0})
nom_ville = ville["capitale"]
id_ville=ville["_id"]
print(nom_ville)
print(id_ville)

# Appel de la fonction get_weatherdata avec la ville récupérée
get_weatherdata(nom_ville)

# Mettre à jour la valeur de la clé "traite" à 1 pour le document récupéré
result = collection.update_one({"_id": id_ville}, {"$set": {"traite": 1}})
if result.modified_count > 0:
    print(f"La valeur de 'traite' pour '{nom_ville}' a été mise à jour avec succès!")
else:
    print(f"La mise à jour de 'traite' pour '{nom_ville}' a échoué.")





