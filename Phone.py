class Phone:
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
        
    def get_desc(self):
        print(self.name+"\n"+self.brand+"\n"+self.camera+"\n"+self.chipset+"\n"+self.os+"\n"+self.ram+"\n"+self.screen+"\n"+self.storage+"\n"+
              self.price+"\n"+self.date+"\n"+self.colors+"\n"+self.width+"\n"+self.height+"\n"+self.screen_dimension
              )