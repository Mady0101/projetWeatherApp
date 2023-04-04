import logging
from json import loads
import pymongo
from app.enum import EnvironmentVariables as EnvVariables
from app.dependecies.mongo import get_instance_db

from kafka import KafkaConsumer


def main():
    try:
        # To consume latest messages and auto-commit offsets
        # client = pymongo.MongoClient("mongodb://root:example@mongo:27017/")
        # db = client["mydatabase"]
        consumer = KafkaConsumer(
            EnvVariables.KAFKA_TOPIC_NAME.get_env(),
            bootstrap_servers=f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        for message in consumer:
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key, message.value))
            data = loads(message.value())
            # result = db["recherche"].insert_one(data)
            # print(result)

    except Exception as e:
        logging.info('Connection successful', e)
