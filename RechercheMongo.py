import pymongo
import re

# Se connecter à la base de données MongoDB dans le conteneur Docker
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.test
# Sélectionner la base de données à utiliser
db = client["mydatabase"]
collection = db["mycollection"]

document = [
    {
        "city_name": "Tunis",
        "temperature": 25.0,
        "pressure": 1013.0,
        "humidity": 50.0,
        "wind_speed": 10.0,
        "wind_direction": "N"
    },
        {
        "city_name": "Paris",
        "temperature": 10.0,
        "pressure": 1000.0,
        "humidity": 70.0,
        "wind_speed": 10.0,
        "wind_direction": "N"
    },
    {
        "city_name": "Touzer",
        "temperature": 30.0,
        "pressure": 990.0,
        "humidity": 80.0,
        "wind_speed": 10.0,
        "wind_direction": "N"
    },
]
y=collection.find_one(document)
#print(y)

# Insertion d'un document dans la collection
if y :
    print("document deja inserer ")

else :
    x = collection.insert_many(document)
    #print(x)
    

nom = input("Entrez le nom a chercher ")

#regex = re.compile(nom, re.IGNORECASE)

result=collection.find( { 'city_name':{'$regex':nom ,'$options': 'i' }} )

#Check if the result is empty using the len() function
result_list = list(result)
#print(result_list)
if len(result_list) == 0:
    print("Pas de document trouvé avec cette ville.")
else:
    # Iterate over the results and print each document
    for rs in result_list:
        print("Nom Ville   : ",rs["city_name"])
        print("Temperature  : ",rs.get("temperature"))
        print("humidité:", rs.get("humidity"))
        print("presion :", rs.get("pressure"))
        print ("------------------")
collection.drop() # pour eliminer la redendance car a chaque fois insert_many est excutée


