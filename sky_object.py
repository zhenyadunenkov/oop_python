#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# В ДАННОМ МОДУЛЕ SKY_OBJECT:
# - описан класс SkyObject, реализовывающий небесное тело.

from math import pi


class SkyObject:

    object_id: str
    right_ascension: float
    declination: float
    azimuth: float
    altitude: float
    apparent_magnitude: float
    color: str

    def __init__(self, right_ascension: list[float], 
                 declination: list[float],
                 magnitude: float, object_id: str ="",
                 spectral_class:str="") -> None:
        
        # инициализируем координаты экваториальной системы
        self.object_id = object_id
        self.right_ascension = self.hms_to_rads(right_ascension)
        self.declination = self.dgrs_to_rads(declination)
        
        self.magnitude = magnitude
        self.color = self.spectral_class_to_color(spectral_class)
        
        
        
    def hms_to_rads(self, hms: list[float]) -> float:
        hrs, ms, s = hms
        grads = hrs * 15 + ms / 60 + s / 3600
        rads = grads * pi / 180
        return rads
        
    def dgrs_to_rads(self, dgrs) -> float:
        sign, grads, ms, s = dgrs
        rads = sign * (grads + ms / 60 + s / 3600)           
        return rads
    
    # задел на будущее
    def spectral_class_to_color(self, sp_class):
        pass
    
    def get_id_coords_and_magnintude(self) -> list[dict]:
        return [{"id": self.object_id,
                "azimuth": self.right_ascension,
                "height": self.declination,
                "magnitude": self.magnitude}]