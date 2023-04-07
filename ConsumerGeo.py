from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import json
from datetime import datetime

# Set up the Kafka consumer configuration
conf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'mygroup', 'auto.offset.reset': 'earliest'}

# Create a Kafka consumer instance
consumer = Consumer(conf)

# Set up the MongoDB client and database
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

# Subscribe to the Kafka topic
consumer.subscribe(['geo'])

while True:
    # Read a message from the Kafka topic
    msg = consumer.poll(timeout=1.0)

    if msg is None:
        continue
    if msg.error():
        # Handle any errors that occur while reading messages
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Reached end of partition')
        else:
            print(f'Error while reading message: {msg.error()}')
    else:
        # Convert the received message from JSON to a Python dictionary
        weather_data = json.loads(msg.value())

        # Insert the weather data into the MongoDB collection
        db.localisation.insert_one(weather_data)

        # Print a message to confirm that the data has been inserted
        print('Inserted weather data into MongoDB')
