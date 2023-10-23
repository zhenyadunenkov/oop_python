#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# В ДАННОМ МОДУЛЕ SKY_MAP:
# - описан класс SkyMap, реализовывающий звёздную карту 
#   следующим образом:
#   -- хранит в себе объекты класса SkyObject и унаследованные от него,
#   -- по запросу отдаёт массив с параметрами видимых звёздных объектов
#      (имя объекта, горизонтальные координаты, видимая звёздная величина),
#      с учётом координат и времени наблюдения, а также минимальной видимой
#      звёздной величины

import sqlite3 # для вычисления юлианской даты

from math import sin, cos, acos, atan2, pi


from sky_object import SkyObject


class SkyMap:

    sky_objects: list[SkyObject]
    
    
    def __init__(self) -> None:
        self.sky_objects = []
    
    
    def add_object(self, sky_object: SkyObject) -> None:
        """
        Метод добавляет небесное тело в массив объектов sky_objects
        """
        if sky_object not in self.sky_objects:
            self.sky_objects.append(sky_object)        
    
    
    def remove_object(self, sky_object: SkyObject) -> None:
        """
        Метод убирает небесное тело из массива объектов sky_objects
        """
        if sky_object in self.sky_objects:
            self.sky_objects.remove(sky_object)    

    def get_map(self, 
                year: int=2023, 
                month: int=10,
                day: int=22,
                universal_time: float=13.5,
                longitude: float=37.616, 
                latitude: float=55.752,
                magnitude: float=0) -> list[str, float]:
        """
        Метод принимает координаты и время наблюдателя и возвращает
        карту звёздного неба (массив, состоящий из названий, координат и
        величин яркости), видимую в соотв. точке в соотв. время        
        """
        
        sky_map = []    

        # собираем параметры (имя, координаты, яркость) каждого звёздного тела
        # в карту (хранит не объекты, а только их параметры):

        for obj in self.sky_objects:
            sky_map.append(*obj.get_id_coords_and_magnintude())
        
        # оставляем в sky_map только объекты нужной яркости
        sky_map = list(filter(lambda obj: 
                              obj["magnitude"] >= magnitude, sky_map))
        
            
        # ЧАСТЬ С ПЕРЕВОДОМ ЭКВАТОРИАЛЬНЫХ (универсальных) КООРДИНАТ 
        # В ГОРИЗОНТАЛЬНЫЕ (зависящие от места наблюдения)
        
        # сначала вычисляем нужные для дальнейших вычислений 
        # промежуточные параметры (модифицированная юлианская дата - mjd, 
        # местное звёздное время - lst):
    
        if month < 10:
            str_month = "0" + str(month)
        else:
            str_month = str(month)

        if day < 10:
            str_day = "0" + str(day)
        else:
            str_day = str(day)

        
            
        today = "-".join([str(year), str_month, str(str_day)])
        query = "select julianday('" + today + "')"
        con = sqlite3.connect(":memory:")
        jd = list(con.execute(query))[0][0]
        mjd = float(jd) - 2400000.5 # модифицированная юлианская дата
        
        t0 = (mjd - 51544.5) / 36525
        a1 = 24110.54841
        a2 = 8640184.812
        a3 = 0.093104
        a4 = 0.0000062
        s0 = a1 + (a2*t0) + (a3*(t0*t0)) - (a4*(t0*t0*t0))
        n_sec = universal_time * 3600
        n_star_sec = n_sec * 366.2422 / 365.2422
        gst = (s0 + n_star_sec) / 3600 * 15  
        
        lst = (gst + longitude) % 360 # местное звёздное время в градусах
        
        # теперь вычисляем координаты для каждого небесного тела в списке
        # часовой угол hour_angle, высоту над горизонтом height
        # азимут azimuth
        # меняем соответственно координаты каждого объекта в sky_map

        for obj in sky_map:
            hour_angle = (lst - obj["azimuth"]) * pi / 180 
            declination = obj["height"]
            zenith = acos(sin(latitude*pi/180) * sin(declination*pi/180) + \
                cos(latitude*pi/180) * cos(declination*pi/180) * cos(hour_angle))
            
            # высота в градусах (первая нужная нам относительная координата)
            height = 90 - zenith/pi*180
            
            # азимут в градусах (вторая нужная нам относительная координата)
            azimuth = atan2(sin(hour_angle)*cos(declination*pi/180),
                       (sin(height*pi/180)*sin(latitude*pi/180)\
                        -sin(declination*pi/180))/cos(latitude*pi/180))
            azimuth = azimuth * 180 /pi + 180
            
            obj["azimuth"] = azimuth
            obj["height"] = height
        
        # оставляем в sky_map только видимые объекты (0 < высота < 180)

        sky_map = list(filter(lambda obj: 
                              obj["height"] >= 0, sky_map))
        sky_map = list(filter(lambda obj: 
                              obj["height"] <= 180, sky_map))

        return sky_map