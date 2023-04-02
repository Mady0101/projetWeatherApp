from confluent_kafka import Consumer
import json
import pymongo
import datetime

# Connexion à la base de données
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
print('Subscribed to database')
collection = db["recherche"]

# Créer un consommateur Kafka qui écoute le sujet "weather"
c=Consumer({'bootstrap.servers':'broker:29092','group.id':'python-consumer'})
c.subscribe(['weather2'])
print('Subscribed to topic')

print('ça va les connexions')

# Boucler sur les messages reçus
while True:
    try:
        msg=c.poll(1.0) #timeout
        if msg is None:
            print('No message')
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data = json.loads(msg.value())
        data['date'] = datetime.datetime.now()
        collection.insert_one(data)
        print(data)
    except Exception as e:
        print('Error: {}'.format(str(e)))
        continue
