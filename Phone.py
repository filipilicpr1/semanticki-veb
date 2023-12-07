import utils
from Table import Table
from datetime import datetime

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

    def create_table_view(self):
        table_view_phone = Table('SPECIFICATION', self.name.replace('_',' '))
        
        table_view_phone.add_row('BRAND', self.brand.capitalize())
        table_view_phone.add_row('CAMERA', self.camera.upper().replace('_',' '))
        table_view_phone.add_row('CHIPSET', self.chipset.capitalize().replace('_',' '))
        table_view_phone.add_row('OS', self.os.capitalize().replace('_',' '))
        table_view_phone.add_row('RAM', self.ram.upper().replace('_',' '))
        table_view_phone.add_row('SCREEN',self.screen.upper().replace('_',' '))
        table_view_phone.add_row('STORAGE',self.storage.upper().replace('_',' '))
        table_view_phone.add_row('PRICE',self.price.replace('_',' ')+" €")
        table_view_phone.add_row('DATE',datetime(int(self.date.split('T')[0].split('-')[0]),int(self.date.split('T')[0].split('-')[1]),int(self.date.split('T')[0].split('-')[2])).strftime("%d.%m.%Y"))
        table_view_phone.add_row('COLORS',self.colors)
        table_view_phone.add_row('RESOLUTION',self.width+'x'++self.height+' px')
        table_view_phone.add_row('SCREEN',self.screen_dimension+' inches')
        
        return table_view_phone.get_string()
