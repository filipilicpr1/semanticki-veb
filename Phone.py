import utils

class Phone:
    def __init__(self, name, brand, camera, chipset, os, ram, screen, storage, screen_dimension, width, height, date, price, colors):
        self.name = name
        self.brand = brand
        self.camera = utils.prepare_camera(camera)
        self.chipset = utils.prepare_chipset(chipset)
        self.os = os
        self.ram = utils.prepare_memory(ram)
        self.screen = screen
        self.storage = utils.prepare_memory(storage)
        self.price = int(price)
        self.date = utils.prepare_date(date)
        self.colors = colors
        self.width = int(width)
        self.height = int(height)
        self.screen_dimension = float(screen_dimension)
        
class MobilePhone:
    def __init__(self, name, brand, camera, chipset, os, ram, screen, storage, screen_dimension, width, height, date, price, colors):
        self.name = name
        self.brand = brand
        self.camera = camera
        self.chipset = chipset
        self.os = os
        self.ram = ram
        self.screen = screen
        self.storage = storage
        self.price = price
        self.date = date
        self.colors = colors
        self.width = width
        self.height = height
        self.screen_dimension = screen_dimension

