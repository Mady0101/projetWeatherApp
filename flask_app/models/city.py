class Weather:
    def __init__(self ,name , value):
        self.name = name 
        self.value = value


class City:
    def __init__(self, id, name, temps, wind , currentTime, temperature, humidity,atmosphericPressure):
        self.id = id
        self.name = name
        self.temps = temps
        self.wind = wind
        self.currentTime = currentTime
        self.temperature = temperature
        self.humidity = humidity
        self.atmosphericPressure = atmosphericPressure

    def __repr__(self):
        return f'<City: {self.name}>'