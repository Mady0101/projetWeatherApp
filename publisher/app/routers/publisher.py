import json
import requests
from app.core.gateways.kafka import Kafka
from app.core.models.message import Message
from app.dependencies.kafka import get_kafka_instance

from fastapi import APIRouter, Depends

router = APIRouter()

countries = ['ariana' , 'paris']

async def get_weatherdata(ville , server: Kafka):
    # Remplacez {API key} par votre propre clé API
    api_key = "0747defefc71f82a572276d367a1be31"
        # URL de l'API avec les paramètres de la ville et de la clé API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}"
            
    # Envoyer une requête GET à l'API
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Extraire les données JSON de la réponse
        data = response.json()
        print(data)
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

        try:
            topic_name = server._topic
            print(topic_name)
            await server.aioproducer.send_and_wait(topic_name, json.dumps(weather_data).encode("ascii"))
        except Exception as e:
            await server.aioproducer.stop()
            raise e
        return 'Message sent successfully'
        
    else:
        # Afficher le code d'erreur HTTP si la requête a échoué
        print(f"Erreur de requête : {response.status_code}")

    print("Jai envoyé")



@router.post("")
async def send(data: Message, server: Kafka = Depends(get_kafka_instance)):
    try:
        topic_name = server._topic
        await server.aioproducer.send_and_wait(topic_name, json.dumps(data.dict()).encode("ascii"))
    except Exception as e:
        await server.aioproducer.stop()
        raise e
    return 'Message sent successfully'


@router.get("/start")
async def start_pub(server: Kafka = Depends(get_kafka_instance)):
    for country in countries:
        await get_weatherdata(country , server)

    return "done"
    # while True:
    #     start = time.time()
    #     for country in range(countries):
    #         get_weatherdata(country)
    #     end = time.time()
    #     while (end - start) < 60*10 :
    #         time.sleep(end - start % 60)
    #         end = time.time()
