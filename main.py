#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ЛАБОРАТОРНАЯ РАБОТА 6

# ЗАДАНИЕ:
    
# Написать программу, которая позволяет:
# - составить карту звёздного неба, 
# - поворачивать её (с поправкой на долготу),
# - отфильтровывать наименее яркие объекты,
# с использованием следующих классов:
# - небесное тело (небесные координаты; видимая звёздная величина),
# - система (несколько связанных небесных тел),
# - карта звёздного неба (массив звёзд и других небесных тел): 
#   -- метод, принимающий значение угла и возвращающий копию карты 
#      звёздного неба, повёрнутую на заданный угол,
#   -- метод, принимающий значение звёздной величины и возвращающий 
#      копию карты звёздного неба, в которой присутствуют только 
#      объекты со звёздной величиной не меньше заданной.

# РЕАЛИЗОВАНО:
# В РАМКАХ ЗАДАЧИ:
# - необходимые классы (SkyObject, SkySystem, SkyMap),
# - метод SkyMap.get_map, возвращающий копию карты (массив с параметрами 
# - каждого небесного тела) в соответствии с:
#   -- широтой и долготой наблюдателя,
#   -- минимальной звёздной величиной,
# ДОПОЛНИТЕЛЬНО:
# - метод SkyMap.get_map также меняет карту в соответствии с 
#   датой и временем (UTC) наблюдения,
# - реализована визуализация звёздной карты (средствами модуля pygame).


# В ДАННОМ МОДУЛЕ MAIN:
# - [не очень изящно] описан класс GUI, с помощью которого происходит визуализация.
# - происходит инициализация объекта SkyMap,
# - парсится файл stars.txt с параметрами некоторых звёзд, создаются
#   соответствующие объекты типа SkyObject, которые затем добавляются
#   в звёздную карту,
# - с помощью объекта GUI осуществляется визуализация звёздной карты.

import pygame # МОДУЛЬ НЕ ВХОДИТ В СТАНДАРТНЫЙ НАБОР!
import re
import time

from math import cos, sin
from sky_map import SkyMap
from sky_object import SkyObject

# ПАРАМЕТРЫ ОКНА ПРИЛОЖЕНИЯ
WIDTH = 1024
HEIGHT = 768

class GUI:
    
    def __init__(self, sky_map: SkyMap) -> None:
        
        pygame.init()

        
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Звёздная карта Бориса')

        self.year = 2023 
        self.month = 10
        self.day = 22
        self.time = 20.0
        self.longitude = 37
        self.latitude = 55
        self.magnitude = 0
        self.names_on = True
        
        self.stars = my_map.get_map(year=self.year,
                                    month=self.month,
                                    day=self.day,
                                    universal_time=self.time,
                                    longitude=self.longitude,
                                    latitude=self.latitude,
                                    magnitude=self.magnitude)
        
        self.needs_processing = False
        

        
        self.selected_setting = "year"
        
        
        self.mainloop()
        pygame.quit()

    
    def mainloop(self) -> None:
        
        self.running = True
        self.need_exit = False
        
        # Можно раскомментировать код ниже, чтобы посмотреть заставку
        # for i in range(2000):
        #     self.stars= my_map.get_map(longitude=i/20)
        #     self.vizualize_map(self.stars)
        #     time.sleep(0.03)

        self.vizualize_map(self.stars)            

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.need_exit:
                    self.running = False
                else:
                    self.event_processor(event)
                    if self.needs_processing:
                        self.vizualize_map(self.stars)
                        self.needs_processing = False  

        
    def event_processor(self, event: pygame.event.Event) -> None:
        
        if event.type == pygame.KEYDOWN:
                        
            if pygame.key.name(event.key) == "escape":
                self.running = False
                self.needs_processing = True
            
            # не самая изящная обработка клавиш, сделанная наспех((
            
            if pygame.key.name(event.key) == "up":
                if self.selected_setting == "year":
                    self.year += 1
                if self.selected_setting == "month":
                    if self.month >= 12:
                        self.month = 1
                        self.year += 1
                    else:
                        self.month += 1
                if self.selected_setting == "day":
                    if self.month == 2 and self.day == 28:
                        self.month += 1
                        self.day = 1
                    elif self.day == 30:
                        if self.month == 12:
                            self.year += 1
                            self.month = 1
                            self.day = 1
                        else:
                            self.month += 1
                            self.day = 1
                    else:
                        self.day +=1
                if self.selected_setting == "universal_time":
                    if round(self.time, ndigits=1) == 23.9:
                        if self.month == 2 and self.day == 28:
                             self.month += 1
                             self.day = 1
                        elif self.day == 30:
                            if self.month == 12:
                                 self.year += 1
                                 self.month = 1
                                 self.day = 1
                            else:
                                 self.month += 1
                                 self.day = 1
                        else:
                             self.day +=1
                        self.time = 0
                    self.time += 0.1
                if self.selected_setting == "longitude":
                    if self.longitude == 90:
                        self.longitude = -90
                    else:
                        self.longitude += 1
                if self.selected_setting == "latitude":
                    if self.latitude == 180:
                        self.latitude = -180
                    else:
                        self.latitude += 1
                if self.selected_setting == "magnitude":
                    self.magnitude += 0.1

                self.needs_processing = True

            if pygame.key.name(event.key) == "down":
                if self.selected_setting == "year":
                    self.year -= 1
                if self.selected_setting == "month":
                    if self.month <= 1:
                        self.month = 12
                        self.year -= 1
                    else:
                        self.month -= 1
                if self.selected_setting == "day":
                    if self.month == 3 and self.day == 1:
                        self.month -= 1
                        self.day = 28
                    elif self.day == 1:
                        if self.month == 1:
                            self.year -= 1
                            self.month = 12
                            self.day = 30
                        else:
                            self.month -= 1
                            self.day = 30
                    else:
                        self.day -= 1
                if self.selected_setting == "universal_time":
                    if round(self.time, ndigits=0) == 0:
                        if self.month == 3 and self.day == 1:
                             self.month -= 1
                             self.day = 28
                        elif self.day == 1:
                            if self.month == 1:
                                 self.year -= 1
                                 self.month = 12
                                 self.day = 30
                            else:
                                 self.month -= 1
                                 self.day = 30
                        else:
                             self.day -=1
                        self.time = 23.9
                    self.time -= 0.1
                if self.selected_setting == "longitude":
                    if self.longitude == -90:
                        self.longitude = 90
                    else:
                        self.longitude -= 1
                if self.selected_setting == "latitude":
                    if self.latitude == -180:
                        self.latitude = 180
                    else:
                        self.latitude -= 1
                if self.selected_setting == "magnitude":
                    if round(self.magnitude, ndigits=1) == 0.0:
                        pass
                    else:
                        self.magnitude -= 0.1

                self.needs_processing = True

            if pygame.key.name(event.key) == "left":
                self.selected_setting = self.prev_set(self.selected_setting)
                self.needs_processing = True
            if pygame.key.name(event.key) == "right":
                self.selected_setting = self.next_set(self.selected_setting)
                self.needs_processing = True
            
            if pygame.key.name(event.key) == "q":
                if self.names_on:
                    self.names_on = False
                else:
                    self.names_on = True
                self.needs_processing = True

        self.stars = my_map.get_map(year=self.year,
                                    month=self.month,
                                    day=self.day,
                                    universal_time=self.time,
                                    longitude=self.longitude,
                                    latitude=self.latitude,
                                    magnitude=self.magnitude)


    def next_set(self, setting: str) -> str:
        sets = ["year", "month", "day", "universal_time", 
                "longitude", "latitude", "magnitude"]
        index = sets.index(setting)
        
        if index == len(sets)-1:
            return sets[0]
        else:
            return sets[index+1]

    def prev_set(self, setting: str) -> str:
        sets = ["year", "month", "day", "universal_time", 
                "longitude", "latitude", "magnitude"]
        index = sets.index(setting)
        
        if index == 0:
            return sets[len(sets)-1]
        else:
            return sets[index-1]

        
    def vizualize_map(self, map: list[str, float]) -> None:

        self.window.fill((0, 0, 0))
        
        my_font = pygame.font.SysFont('Sans', 10)


        for star in map:
            x = 800 * (star["height"] / 90) * cos(star["azimuth"]) + int(WIDTH/2)
            y = 800 * (star["height"] / 90) * sin(star["azimuth"]) + int(HEIGHT/2)

            r = star["magnitude"] * 0.5

            if self.names_on:
                text_surface = my_font.render(star["id"], False, (255, 0, 0))
                self.window.blit(text_surface, (x, y))
               
            pygame.draw.circle(self.window, (255, 255, 255), (x, y), r)
            
        
        self.add_interface()
            
        pygame.display.flip()
        
    def add_interface(self):
        pygame.draw.rect(self.window, 
                         (127, 127, 127), 
                         (0, HEIGHT-110, WIDTH, 100))
        
        font = pygame.font.SysFont('Sans', 15)
        text = "Дата: " + str(self.year) +" "+ str(self.month) + " " + \
            str(self.day) + \
            "      Время (часы UTC): " + str(round(self.time,ndigits=1)) + "      Долгота: " +\
            str(self.longitude) + "      Широта: " + str(self.latitude) + \
            "      Минимальная видимая яркость: " + str(round(self.magnitude, ndigits=2))
        
        text_surface = font.render(text, False, (255, 255, 255))

        y = HEIGHT-75    

        if self.selected_setting == "year":
            x = 70
        elif self.selected_setting == "month":
            x = 100
        elif self.selected_setting == "day":
            x = 120
        elif self.selected_setting == "universal_time":
            x = 290
        elif self.selected_setting == "longitude":
            x = 400
        elif self.selected_setting == "latitude":
            x = 500
        elif self.selected_setting == "magnitude":
            x = 760

        # дописываем подсказки
        instr = "ESC выход  ← → сменить настраиваемый параметр,  ↑ ↓ настройка, Q вкл/выкл подписи"
        instructions = font.render(instr, False, (255, 255, 0))


        pygame.draw.circle(self.window, (255, 0, 255), (x, y), 12)

        self.window.blit(text_surface, (10, HEIGHT-85))
        self.window.blit(instructions, (9, HEIGHT-105))

        

my_map = SkyMap()


with open("stars.txt", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        parameters = line.split("\t")
        
        r_asc = parameters[3]
        hrs = float(re.search("\d*(?=ч)", r_asc).group(0))
        m = float(re.search("\d*(?=м)", r_asc).group(0))
        s = float(re.search("(?<=м).*(?=с)", r_asc).group(0))
        
        decl = parameters[4]
        if decl[0] == "+":
            sign = 1
        else:
            sign = -1
            
        grad = float(re.search("\d*(?=°)", decl).group(0))
        mins = float(re.search("\d*(?=′)", decl).group(0))
        secs = float(re.search("(?<=′).*(?=″)", decl).group(0))
        
        my_map.add_object(SkyObject(object_id=parameters[0],
                                    spectral_class=parameters[2],
                                    right_ascension = [hrs, m, s], 
                                    declination = [sign, grad, mins, secs], 
                                    magnitude=float(parameters[1])))
        
        

app = GUI(my_map)

