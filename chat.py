from OWLManager import OWLManager
from SPARQLManager import SPARQLManager
from UI.Menu import Menu
from UI.ConsoleUserInteraction import ConsoleUserInterface
from command_pattern.PhonesCommands import PhoneByBrandDatePrice, PhoneByBrandOS, PhoneByCamera, PhoneByChipsetRamStorage,PhoneByScreenSizeAndResolution, PhonesByColor, PhoneWithMinPriceForBrand, CheapestPhoneWithBestCameraByBrandDate, CheapestPhoneWithCameraAndYoungerThanDate, ColorsForPhoneModel

user_interface = ConsoleUserInterface()
sparql_manager = SPARQLManager(owl_manager=OWLManager("GoodRelationsPopulated.owl"))

phones_by_brand_date_price = PhoneByBrandDatePrice(user_interface, sparql_manager)
phones_by_brand_os = PhoneByBrandOS(user_interface, sparql_manager)
phones_by_camera = PhoneByCamera(user_interface, sparql_manager)
phones_by_chipset_ram_storage = PhoneByChipsetRamStorage(user_interface, sparql_manager)
phones_by_screen_size_resolution = PhoneByScreenSizeAndResolution(user_interface, sparql_manager)
phones_by_color = PhonesByColor(user_interface, sparql_manager)
phones_with_min_price_for_brand = PhoneWithMinPriceForBrand(user_interface, sparql_manager)
phone_with_best_camera_by_brand_cheapest_one = CheapestPhoneWithBestCameraByBrandDate(user_interface, sparql_manager)
cheapest_phone_with_camera_younger_than = CheapestPhoneWithCameraAndYoungerThanDate(user_interface, sparql_manager)
all_colors_for_phone_model = ColorsForPhoneModel(user_interface, sparql_manager)

commands = [phones_by_brand_date_price, phones_by_brand_os, phones_by_camera, phones_by_chipset_ram_storage, phones_by_screen_size_resolution, phones_by_color, 
            phones_with_min_price_for_brand, phone_with_best_camera_by_brand_cheapest_one, cheapest_phone_with_camera_younger_than, all_colors_for_phone_model]

menu = Menu(user_interface, commands)

menu.run()