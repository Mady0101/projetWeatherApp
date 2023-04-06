import time

from app.core.gateways.kafka import Kafka
from app.dependencies.kafka import get_kafka_instance
from app.enum import EnvironmentVariables
from app.routers import publisher





from dotenv import load_dotenv

from fastapi import Depends, FastAPI, Request

load_dotenv()


app = FastAPI(title='Kafka Publisher API')
kafka_server = Kafka(
    topic=EnvironmentVariables.KAFKA_TOPIC_NAME.get_env(),
    port=EnvironmentVariables.KAFKA_PORT.get_env(),
    servers=EnvironmentVariables.KAFKA_SERVER.get_env(),
)





# Connexion à la base de données MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["mydatabase"]
# collection = db["choix"]



# ville = collection.find_one({"traite": 0})
# nom_ville = ville["capitale"]
# id_ville=ville["_id"]
# print(nom_ville)
# print(id_ville)

# Appel de la fonction get_weatherdata avec la ville récupérée


# Mettre à jour la valeur de la clé "traite" à 1 pour le document récupéré
# result = collection.update_one({"_id": id_ville}, {"$set": {"traite": 1}})
# if result.modified_count > 0:
#     print(f"La valeur de 'traite' pour '{nom_ville}' a été mise à jour avec succès!")
# else:
#     print(f"La mise à jour de 'traite' pour '{nom_ville}' a échoué.")










@app.on_event("startup")
async def startup_event():
    await kafka_server.aioproducer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_server.aioproducer.stop()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get('/')
def get_root():
    return {'message': 'API is running...'}


# @app.get('/start')
# async def start_pub():
#     await kafka_server.aioproducer.start()
#     for country in range(countries):
#         get_weatherdata(country)
#     # while True:
#     #     start = time.time()
#     #     for country in range(countries):
#     #         get_weatherdata(country)
#     #     end = time.time()
#     #     while (end - start) < 60*10 :
#     #         time.sleep(end - start % 60)
#     #         end = time.time()

        



app.include_router(
    publisher.router,
    prefix="/producer",
    tags=["producer"],
    dependencies=[Depends(get_kafka_instance)],
)
