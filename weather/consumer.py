import time
from kafka import KafkaConsumer
import requests
import json
from pprint import pprint 
from kafka import errors
import sys

try:
        city = input("Enter city name: ")
        consumer = KafkaConsumer(
            'Test',
            bootstrap_servers=['broker:29092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: x.decode('utf-8')
        )

        while True:
            
# Look for message with temperature for the requested city in Kafka topic
            for message in consumer:
                if message.value['city'] == city:
                    current_temperature = message.value['temperature']
                    print("Message with temperature %s for city %s found in topic" % (current_temperature, city))
                    break

            # Fetch current temperature for the requested city from openAPI weather
            response = requests.get("https://api.openweathermap.org/data/2.5/weather?q={}&appid=d7094c960654ec3baf58f5e3e311fcf4&units=metric".format(city))
            actual_temperature = response.json()["main"]["temp"]

            # Compare expected temperature value from Kafka message with actual temperature value from openAPI weather
            if current_temperature == actual_temperature:
                print("Test passed")
            else:
                print("Test failed")

except Exception as e:
        print(f"Error: {e}")

finally:
        consumer.close()


