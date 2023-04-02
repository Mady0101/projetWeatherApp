import requests
import pymongo

url = "https://restcountries.com/v3.1/all"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    client = pymongo.MongoClient("mongodb://mongodb:27017/")
    db = client["mydatabase"]
    collection = db["capitales"]

    # Get the current count of documents in the collection
    current_count = collection.count_documents({})
    if current_count==0:
        for country in data:
            if 'capital' in country:
                capital = country['capital'][0]
                capital_doc = {"_id": current_count + 1, "nom": capital}
                collection.insert_one(capital_doc)

                # Increment the counter
                current_count += 1

else:
    print("Failed to get data from API")

for capital in collection.find():
    print(capital)


# Demander à l'utilisateur de saisir une capitale
nom_capitale = input("Entrez le nom d'une capitale : ")
# Récupérer l'ID et le nom de la capitale à partir de la collection "capitales"
capitale = collection.find_one({"nom": nom_capitale})
if capitale:
    capitale_id = capitale["_id"]
else:
    print("Capitale introuvable dans la base de données")
    exit()

nouvelle_collection = db["choix"]
document = {"capitale_id": capitale_id,"capitale": nom_capitale, "traite": 0}
nouvelle_collection.insert_one(document)

for capital in nouvelle_collection.find():
    print(capital)
