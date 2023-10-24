# ЛАБОРАТОРНАЯ РАБОТА 6

# ЗАДАНИЕ:
    
Написать программу, которая позволяет:
- составить карту звёздного неба, 
- поворачивать её (с поправкой на долготу),
- отфильтровывать наименее яркие объекты,
  
с использованием следующих классов:

- небесное тело (небесные координаты; видимая звёздная величина),
- система (несколько связанных небесных тел),
- карта звёздного неба (массив звёзд и других небесных тел): 
  -- метод, принимающий значение угла и возвращающий копию карты 
      звёздного неба, повёрнутую на заданный угол,
  -- метод, принимающий значение звёздной величины и возвращающий 
      копию карты звёздного неба, в которой присутствуют только 
      объекты со звёздной величиной не меньше заданной.

# РЕАЛИЗОВАНО:

В РАМКАХ ЗАДАЧИ:
- необходимые классы (SkyObject, SkySystem, SkyMap),
- метод SkyMap.get_map, возвращающий копию карты (массив с параметрами 
- каждого небесного тела) в соответствии с:
  -- широтой и долготой наблюдателя,
  -- минимальной звёздной величиной,
  
ДОПОЛНИТЕЛЬНО:
- метод SkyMap.get_map также меняет карту в соответствии с 
  датой и временем (UTC) наблюдения,
- реализована визуализация звёздной карты (средствами модуля pygame).

# ЗАМЕЧАНИЯ
Модуль Pygame, средствами которого реализована визуализация, нужно установить отдельно

# СТРУКТУРА ПРОЕКТА

1. В модуле main описан класс GUI, с помощью которого происходит визуализация, 
   парсится файл stars.txt с параметрами некоторых звёзд, создаются соответствующие 
   объекты типа SkyObject, которые затем добавляются в звёздную карту, осуществляется
   визуализация звёздной карты.

2. В модуле sky_object описан класс SkyObject (реализация небесного тела).

3. В модуле sky_system описан класс SkySystem, унаследованный от класса SkyObject
   (реализация системы небесных тел).

4. В модуле sky_map описан класс SkyMap (реализация звёздной карты), который 
   - хранит в себе объекты класса SkyObject и унаследованные от него,
   - по запросу отдаёт массив с параметрами видимых звёздных объектов
  (имя объекта, горизонтальные координаты, видимая звёздная величина),
  учётом координат и времени наблюдения, а также минимальной видимой
  звёздной величины.

5. Модуль test содержит тесты, демонстрирующие реализацию классов и методов в рамках
   лабораторной работы.

6. Файл stars.txt содержит набор звёзд с параметрами, из которых в модуле main собирается
   звёздная карта.
