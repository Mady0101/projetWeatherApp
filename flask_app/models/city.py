class Weather:
    def __init__(self ,name , value):
        self.name = name 
        self.value = value


class City:
    def __init__(self, id, name, weather:Weather, wind , currentTime, temperature, humidity,atmospheric_pressure):
        self.id = id
        self.name = name
        self.weather = weather
        self.wind = wind
        self.currentTime = currentTime
        self.temperature = temperature
        self.humidity = humidity
        self.atmospheric_pressure = atmospheric_pressure

    def __repr__(self):
        return f'<City: {self.name}>'