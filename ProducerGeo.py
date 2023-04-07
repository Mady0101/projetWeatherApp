import json
import requests
from confluent_kafka import Producer
import geocoder
import time

# Set up the Kafka producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Set the time interval to 30 minutes
interval = 30 * 60

while True:
    # Get the current location coordinates
    g = geocoder.ip('me')
    lat, lon = g.latlng

    # Get the weather data from the OpenWeather API
    api_key = '0747defefc71f82a572276d367a1be31'
    city_name = g.city
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'

    response = requests.get(url)
    data = response.json()

    # Create a dictionary to store the weather data
    weather_data = {
        'latitude': lat,
        'longitude': lon,
        'city': data['name'],
        'temperature': int(data['main']['temp'] - 273.15),
        'weather': data['weather'][0]['main'],
        'wind_speed': data['wind']['speed'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure']
    }

    # Convert the dictionary to JSON
    weather_data_json = json.dumps(weather_data)

    # Send the weather data to the Kafka topic
    producer.produce('geo', weather_data_json.encode('utf-8'))

    # Wait for any outstanding messages to be delivered and delivery reports received
    producer.flush()

    # Wait for 30 minutes before running the producer code again
    time.sleep(interval)

# Close the Kafka producer
producer.close()
