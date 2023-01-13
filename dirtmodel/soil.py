from math import exp
from dataclasses import dataclass


@dataclass(frozen=True)
class SoilParameters:
    humus_level: float
    looseness: float
    volume: float
    plant_absorb: float

    def get_max_water_level(self):
        return self.volume * self.humus_level * 1 / self.looseness

    # water evaporates like de^(-water_level * 1 / max_water_level)/ dwater_level
    def get_water_evaporation(self, water_level):
        delta = 0.01
        delta_inv = 100
        return (exp((water_level + delta) * 1 / self.humus_level) - exp(water_level * 1 / self.humus_level)) * delta_inv

    def get_water_absorption(self, water_level):
        return self.plant_absorb

    def get_water_loss(self, water_level):
        return self.looseness * water_level / 10


class Soil:
    water_level: float
    tick_ = 0

    def __init__(self, params: SoilParameters):
        self.params = params
        self.water_level = params.get_max_water_level() / 5

    def irrigate(self, water_amount):
        self.water_level += min(water_amount, self.params.get_max_water_level() - self.water_level)

    def tick(self):
        self.water_level -= self.params.get_water_loss(self.water_level)
        if self.tick_ % 10 == 0:
            self.water_level -= self.params.get_water_evaporation(self.water_level)
        self.water_level -= self.params.get_water_absorption(self.water_level)
        self.water_level = max(0, self.water_level)
        self.tick_ += 1

    def get_water_level(self):
        return self.water_level
