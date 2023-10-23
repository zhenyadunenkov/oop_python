#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# В ДАННОМ МОДУЛЕ SKY_SYSTEM:
# - описан класс SkySystem, унаследованный от класса SkyObject и
#   реализовывающий систему небесных тел.

from sky_object import SkyObject


class SkySystem(SkyObject):
    
    objects: list[SkyObject]
    

    def __init__(self) -> None:
        self.objects = []


    def add_object(self, sky_object: SkyObject) -> None:
        
        if sky_object in self.objects:
            return
        else:
            self.objects.append(sky_object)
        
            
    def remove_object(self, sky_object: SkyObject) -> None:
        
        if sky_object in self.objects:
            self.objects.remove(sky_object)
        else:
            return
        
    def get_id_coords_and_magnintude(self) -> list[dict]:
        result = []
        for obj in self.objects:
            result += obj.get_id_coords_and_magnintude()
        return result