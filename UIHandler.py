from SPARQLManager import SPARQLManager
from datetime import datetime

class UIHandler:
    def __init__(self, sparql_manager: SPARQLManager):
        self.sparql_manager = sparql_manager

    def run(self):
        while True:
            self.show_options()
            option, success = self.get_option(input())

            if not success or option < 0 or option > 10:
                print("Unknown option, try again\n")
                continue

            if option == 0:
                print("Goodbye")
                break

            self.handle_option(option)

    def show_options(self):
        options = "Choose an option:\n"
        options += "1. Search phones by brand, date and price\n"
        options += "2. Search phones by chipset, ram and storage\n"
        options += "3. Search phones by brand and OS\n"
        options += "4. Find cheapest phone with best camera by brand and date\n"
        options += "5. Search phones by screen size and resolution\n"
        options += "0. Exit\n"
        print(options)

    def get_option(self, input):
        try:
            option = int(input)
            return option, True
        except:
            return -1, False
        
    def handle_option(self, option):
        if option == 1:
            brand = self.get_string_input("Enter brand name: ")
            date = self.get_date_input("Enter min date(yyyy-MM-dd): ")
            price = self.get_int_input("Enter max price: ")
            phones = self.sparql_manager.get_phones_by_brand_date_price(brand, date, price)
            for p in phones :
                print(p.name)
            return
        
        if option == 2:
            chipset = self.get_string_input("Enter chipset manufacturer: ")
            ram = self.get_int_input("Enter ram(GB): ")
            storage = self.get_int_input("Enter storage(GB): ")
            phones = self.sparql_manager.get_phones_by_chipset_ram_storage(chipset, ram, storage)
            for p in phones :
                print(p.name)
            return
        
        if option == 3:
            brand = self.get_string_input("Enter brand name: ")
            os = self.get_string_input("Enter OS: ")
            phones = self.sparql_manager.get_phones_by_brand_os(brand, os)
            for p in phones :
                print(p.name)
            return
        
        if option == 4:
            brand = self.get_string_input("Enter brand name: ")
            date = self.get_date_input("Enter min date(yyyy-MM-dd): ")
            price = self.get_int_input("Enter max price: ")
            phones = self.sparql_manager.get_phone_with_best_camera_by_brand_date_price(brand, date, price)
            for p in phones :
                print(p.name)
            return
        
        if option == 5:
            size = self.get_float_input("Enter screen size(inches): ")
            width = self.get_int_input("Enter width: ")
            height = self.get_int_input("Enter height: ")
            phones = self.sparql_manager.get_phones_by_screen_size_resolution(size, width, height)
            for p in phones :
                print(p.name)
            return
        
        print("Unknown option")

    def get_string_input(self, message=""):
        return input(message)
    
    def get_int_input(self, message=""):
        while True:
            try:
                value = int(input(message))
                return value
            except:
                print("Value " + value + " is not valid, try again")

    def get_float_input(self, message=""):
        while True:
            try:
                value = float(input(message))
                return value
            except:
                print("Value " + value + " is not valid, try again")

    def get_date_input(self, message=""):
        while True:
            try:
                value = input(message)
                datetime.fromisoformat(value)
                return value + "T:00:00:00"
            except:
                print("Value " + value + " is not valid, try again")