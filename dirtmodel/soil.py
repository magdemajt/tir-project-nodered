from math import exp
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class SoilParameters:
    humus_level: float
    looseness: float
    volume: float
    plant_absorb: float

    def get_max_water_level(self):
        return self.volume * self.humus_level * 1 / self.looseness

    def get_water_absorption(self):
        return self.plant_absorb

    def get_water_losseness(self, water_level):
        return self.looseness * water_level / 100

    def get_water_loss(self, water_level):
        return self.get_water_losseness(water_level)*2+self.get_water_absorption()


@dataclass
class Weather:
    temperature: float
    humidity: float
    wind_speed: float

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.temperature

    def get_wind_speed(self):
        return self.temperature

    def get_weather_factor(self):
        return ((self.temperature-10)/20)*0.5+((100-self.humidity)/100)*0.3+((self.wind_speed/30)*0.2)

    def check_weather(self):
        self.temperature = max(
            10, min(30, self.temperature+random.random()/2-1/4))
        self.humidity = max(0, min(100, self.humidity+random.random()*1-0.5))
        self.wind_speed = max(0, min(30, self.humidity+random.random()*1-0.5))


class Soil:
    water_level: float
    weather: Weather
    tick_ = 0

    def __init__(self, params: SoilParameters):
        self.params = params
        self.weather = Weather(20, 50, 15)
        self.water_level = params.get_max_water_level() / 5

    def irrigate(self, water_amount):
        self.water_level += min(water_amount,
                                self.params.get_max_water_level() - self.water_level)


    def tick(self):
        self.weather.check_weather()
        water_lost=self.params.get_water_loss(self.water_level)*self.weather.get_weather_factor()
        self.water_level = max(0,self.water_level-water_lost)
        self.tick_ += 1

    def get_water_level(self):
        return self.water_level
