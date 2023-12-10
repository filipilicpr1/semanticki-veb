from command_pattern.ICommand import Command
from langchain.chains import GraphSparqlQAChain
from langchain.chat_models import ChatOpenAI
from langchain.graphs import RdfGraph

class PhoneByBrandDatePrice(Command) :
    def execute(self):
        brand = self.user_interface.get_string_input("Enter brand name: ")
        date = self.user_interface.get_date_input("Enter min date(yyyy-MM-dd): ")
        price = self.user_interface.get_int_input("Enter max price: ")
        phones = self.sparql_manager.get_phones_by_brand_date_price(brand, date, price)
        
        if len(phones) == 0 : 
            self.user_interface.show("Phone with that brand and price younger than "+ date.strftime("%d.%m.%Y") +" does not exists") 
            return
        
        for p in phones : self.user_interface.show(p.create_table_view())
    
    def description(self):
        return "Search phones by brand, date and price"
    
class PhoneByChipsetRamStorage(Command):
    def execute(self):
        chipset = self.user_interface.get_string_input("Enter chipset manufacturer: ")
        ram = self.user_interface.get_int_input("Enter ram(GB): ")
        storage = self.user_interface.get_int_input("Enter storage(GB): ")
        phones = self.sparql_manager.get_phones_by_chipset_ram_storage(chipset, ram, storage)
        
        if len(phones) == 0: 
            self.user_interface.show("Phone with that chipset and ram does not exists") 
            return
        
        for p in phones : self.user_interface.show(p.create_table_view())
            
    def description(self):
        return "Search phones by chipset, ram and storage"
    
class PhoneByBrandOS(Command):
    def execute(self):
        brand = self.user_interface.get_string_input("Enter brand name: ")
        os = self.user_interface.get_string_input("Enter OS: ")
        phones = self.sparql_manager.get_phones_by_brand_os(brand, os)
        
        if len(phones) == 0: 
            self.user_interface.show("Phone with that barnd and os does not exists") 
            return
        
        for p in phones : self.user_interface.show(p.create_table_view())
    
    def description(self):
        return "Search phones by brand and OS"
    
class CheapestPhoneWithBestCameraByBrandDate(Command):
    def execute(self):
        brand = self.user_interface.get_string_input("Enter brand name: ")
        date = self.user_interface.get_date_input("Enter min date(yyyy-MM-dd): ")
        price = self.user_interface.get_int_input("Enter max price: ")
        phones = self.sparql_manager.get_phone_with_best_camera_by_brand_date_price(brand, date, price)
        
        if len(phones) == 0: 
            self.user_interface.show("Phone with that specification does not exists") 
            return
        
        for p in phones : self.user_interface.show(p.create_table_view())
    
    def description(self):
        return "Find cheapest phone with best camera by brand, date and max price"
    
class PhoneByScreenSizeAndResolution(Command):
    def execute(self):
        size = self.user_interface.get_float_input("Enter screen size(inches): ")
        width = self.user_interface.get_int_input("Enter width: ")
        height = self.user_interface.get_int_input("Enter height: ")
        phones = self.sparql_manager.get_phones_by_screen_size_resolution(size, width, height)
        
        if len(phones) == 0: 
            self.user_interface.show("Phone with that screen size and resolution does not exists") 
            return
        
        for p in phones : self.user_interface.show(p.create_table_view())
    
    def description(self):
        return "Search phones by screen size and resolution"
    
class PhoneByCamera(Command):
    def execute(self):
        camera = self.user_interface.get_float_input("Enter camera(mpx) : ")
        phones = self.sparql_manager.get_all_phones_with_camera(camera)
        
        if len(phones) == 0: 
            self.user_interface.show("Phone with that camera does not exists") 
            return
        
        for p in phones : self.user_interface.show(p.create_table_view())
            
    def description(self):
        return "Search phones with specified camera"
    
class PhonesByColor(Command):
    def execute(self):
        color = self.user_interface.get_string_input("Enter color : ")
        phones = self.sparql_manager.get_all_phones_with_color(color)
        
        if len(phones) == 0: 
            self.user_interface.show("Phone with that color does not exists") 
            return
        
        for p in phones : self.user_interface.show(p.create_table_view())
    
    def description(self):
        return "Search phones with specified color"
    
class ColorsForPhoneModel(Command):
    def execute(self):
        model = self.user_interface.get_string_input("Enter model : ")
        colors = self.sparql_manager.get_color_for_specific_phone_model(model)
        
        self.user_interface.show_list_of_colors(colors)
        
    def description(self):
        return "Search colors for phone model"
        
class PhoneWithMinPriceForBrand(Command):
    def execute(self):
        brand = self.user_interface.get_string_input("Enter brand name : ")
        date = self.user_interface.get_date_input("Enter min date(yyyy-MM-dd): ")
        phone = self.sparql_manager.get_phone_with_min_price_for_brand(brand,date)
        
        if phone is None:
            self.user_interface.show("Phone with that brand does not exists")
            return
        
        self.user_interface.show(phone.create_table_view())
        
    def description(self):
        return "Search cheapest phone for brand"
        
class CheapestPhoneWithCameraAndYoungerThanDate(Command):
    def execute(self):
        camera = self.user_interface.get_float_input("Enter camera(mpx) : ")
        date = self.user_interface.get_date_input("Enter min date(yyyy-MM-dd): ")
        phone = self.sparql_manager.get_phone_with_specified_camera_with_min_price_but_younger_than(date,camera)
        
        if phone is None:
            self.user_interface.show("Phone with that camera and date does not exists")
            return
        
        self.user_interface.show(phone.create_table_view())
        
    def description(self):
        return "Search phones with specified camera younger than specified date"
    
class NaturalLanguageQuery(Command):
    def __init__(self, user_interface, sparql_manager) -> None:
        super().__init__(user_interface, sparql_manager)

        self.graph = RdfGraph(
            source_file="GoodRelationsPopulatedLite.ttl",
            standard="owl",
            serialization="ttl",
            local_copy="GoodRelationsPopulatedLite.ttl",
        )
        self.graph.load_schema()
        self.chain = GraphSparqlQAChain.from_llm(
            ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0), graph=self.graph, verbose=True,
        )

        self.context = """ Use following rules:
                    Don't exclude any results, I want the full list. 
                    Phone must be a rdfs:subClassOf http://www.co-ode.org/ontologies/ont.owl#SmartPhone. 
                    For hasBrand use http://www.co-ode.org/ontologies/ont.owl#hasBrand. 
                    Brand name in query must be written in all lowercase.
                    Brand name represents object for hasBrand. 
                    For hasPrice use http://www.co-ode.org/ontologies/ont.owl#hasPrice.
                    Camera Mpx is type of xsd:double.
                    All prices are in euros."""

    def execute(self):
        query = self.user_interface.get_string_input("Enter query: ")
        print(self.chain.run(query + self.context))
        
    def description(self):
        return "Write query in natural language (experimental)"