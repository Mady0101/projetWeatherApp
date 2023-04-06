from kafka import KafkaProducer
import requests
import json
from pprint import pprint 
from kafka import errors
import sys

# set the Kafka broker information
#el locolhost hiya el hostname mtaa el broker eli bech nabathoulou el message w 9092 houwa el port mteou

bootstrap_servers = ['broker:29092']

try:
# create a KafkaProducer object
#producer hiya variable tekhou l'objet kafkaproducer eli saretlou el initialisation avec bootstrap_servers et value_seralizer
#lezem tsir serialisation khater el message kafka en byte yetkra donc staamalna fonction lambda tekhou el value mtaa el message 
#el message esmou m w baed tsir convertion lel JSON-string bel json.dumps(m) w baed encodage lel byte bel utf-8 
 producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda m: json.dumps(m).encode('utf-8'))

except Exception as e:
    print("Failed to connect to Kafka broker: {}".format(e))
    sys.exit(1)

while True:
   city = input ("Entrez votre ville : ")

   url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=d7094c960654ec3baf58f5e3e311fcf4&units=metric".format(city)

   #l'objet retourné fel response

   response = requests.get(url)

   #el valeur 200 maaneha succès 
   if response.status_code == 200:
      #print(response)
      data = response.json()
      #pprint taamel présentation mtaa json bi facon hlowa
      #pprint(data)
      temp = data["main"]["temp"]
      #wind = data["wind"]["speed"]
      #latitude = data["coord"]["lat"]
      #longitude = data["coord"]["lon"]
      # send the temperature data to the Kafka broker
      break
   else: 
      print("Invalid city name, please try again.")

topic = "Test"
try:
        producer.send(topic, {'temperature': temp, "city": city})

        producer.flush()  # wait for all messages to be sent
        print("data sent successfully!")

except errors.NoBrokersAvailable as e:
        print("Failed to send data to Kafka broker: {}".format(e))
 
   #print("Temperature :", temp, "degree celcius")
   #print("Wind Speed :", wind, "m/s")
   #print("Latitude :", latitude)
   #print("Longitude :", longitude)



    