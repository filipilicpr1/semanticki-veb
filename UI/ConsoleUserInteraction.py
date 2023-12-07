from datetime import datetime

class ConsoleUserInterface:
    def get_option(self, input):
        try:
            option = int(input)
            return option, True
        except:
            return -1, False
        
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
                date = datetime.fromisoformat(value)
                return date
            except:
                print("Value " + value + " is not valid, try again")
                
    def show_list_of_colors(self, colors):
        if len(colors) == 0 or colors is None :
            print("This model does not exists\n")
            return 
        
        print("\nModel is available in : ")
        for c in colors : print(c.strip())
        print("\n")
            
    def show(self, string):
        print(string)
        
    def show_options(self, options) :
        for key, values in options.items() :
            print(str(key) + '. ' + values.description())