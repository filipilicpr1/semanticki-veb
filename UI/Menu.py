class Menu:
    def __init__(self, user_interface, commands):
        self.user_interface = user_interface
        self.commands = commands

    def run(self):
        while True:
            try:
                dict_options = self.show_menu()
                option, success = self.user_interface.get_option(input())

                if not success or option < 0 or option > 10:
                    self.user_interface.show("Unknown option, try again\n")
                    continue

                if option == 0:
                    self.user_interface.show("Goodbye")
                    break

                option_for_execute = self.handle_option(option, dict_options)
                if option_for_execute is not None :
                    option_for_execute.execute()
            except Exception as e:
                print(e)

    def show_menu(self):
        self.user_interface.show("Choose an option:\n")
        
        dict_options = dict()
        i = 1
        for c in self.commands :
            dict_options[i] = c
            i += 1
        
        self.user_interface.show_options(dict_options)
        return dict_options
    
    def handle_option(self, option, dict_options):
        try :
            return dict_options[option]
        except :
            self.user_interface.show("That command does not exists")
            return None

    