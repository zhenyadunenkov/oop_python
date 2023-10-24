#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sky_map import SkyMap
from sky_object import SkyObject 
from sky_system import SkySystem

# создаём небесные тела
betelgeuse = SkyObject(right_ascension = [5, 55, 10.04], 
                       declination = [1, 7, 24, 0.08], 
                       magnitude = 1, 
                       object_id="Betelgeuse")

polaris = SkyObject(right_ascension = [2, 31, 48.7], 
                       declination = [1, 89, 15, 51.0], 
                       magnitude = 1.97, 
                       object_id="Polaris")

mock_star = SkyObject(right_ascension = [6, 45, 8.92], 
                       declination = [1, 23, 15, 45.0], 
                       magnitude = 1.46, 
                       object_id="Mock Star")
 
mock_planet = SkyObject(right_ascension = [6, 45, 8.92], 
                       declination = [1, 23, 15, 45.0], 
                       magnitude = 0, 
                       object_id="Mock Planet")

# создаём небесную систему и добавляем в неё соответствующие объекты
mock_planet_system = SkySystem()

mock_planet_system.add_object(mock_star)
mock_planet_system.add_object(mock_planet)

# создаём карту и добавляем в неё созданные объекты (2 звезды и 
# планетную систему)

m = SkyMap()
m.add_object(betelgeuse)
m.add_object(polaris)
m.add_object(mock_planet_system)

# ПРОВЕРЯЕМ РАБОТУ МЕТОДА GET_MAP
# без аргументов (по умолчанию вернёт все объекты, поправленные на широту 
# и долготу Москвы)
print("\nКарта небесных тел по умолчанию (с поправкой на координаты Москвы):\n")
print(m.get_map())

# с поправкой на широту и долготу Нью-Йорка
print("\nКарта небесных тел по умолчанию (с поправкой на координаты Нью-Йорка):\n")
print(m.get_map(longitude=74, latitude=40))

# с минимальной яркостью (без mock_planet и Бетельгейзе)
print("\nКарта небесных тел, отвечающих критерию минимальной яркости:\n")
print(m.get_map(magnitude=1.1))

