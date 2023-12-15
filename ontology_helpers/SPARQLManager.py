from rdflib import XSD, Literal, RDF
from .OWLManager import OWLManager
from .sparql_query_helper import sparql_query_select_part, sparql_query_optional_part, create_init_bindings_for_sparql_query, get_list_of_phones_from_sparql_query
import constants

class SPARQLManager:
    def __init__(self, owl_manager : OWLManager):
        self.owl_manager = owl_manager
        self.graph = owl_manager.graph
        self.object_properties = owl_manager.object_properties

    def get_phones_by_brand_date_price(self, brand, date, max_price):
        brand_individual = self.owl_manager.get_individual(brand)
        if not brand_individual:
            raise Exception("Error finding brand with name: " + brand)
        
        date_literal = Literal(date, datatype=XSD.dateTime)
        max_price_literal = Literal(max_price)

        query = sparql_query_select_part + """
                where {{ ?name ?hasBrand ?brand .
                         ?name ?hasPrice ?price . 
                         filter (?price <= ?maxPrice) .
                         ?name ?hasDate ?date .
                         filter (?date >= ?minDate) .
                    """ + sparql_query_optional_part + """
                }}
                order by desc(?price)
                """

        init_bindings = create_init_bindings_for_sparql_query(self)
        init_bindings['brand'] = brand_individual
        init_bindings['maxPrice'] = max_price_literal
        init_bindings['minDate'] = date_literal

        result = self.graph.query(query, initBindings = init_bindings)
        return get_list_of_phones_from_sparql_query(result)

    def get_phones_by_chipset_ram_storage(self, chipset, ram, storage):
        chipset_class = self.owl_manager.get_chipset_class(chipset)
        ram_literal = Literal(ram)
        storage_literal = Literal(storage)
        if not chipset_class:
            raise Exception("Error finding chipset class with name: " + chipset)
        
        query = sparql_query_select_part + """
                where {{ ?name ?hasChipset ?chipset . 
                         ?chipset ?type  ?chipsetClass . 
                         ?name ?hasRam ?ram . 
                         ?ram ?hasMemory ?ramGB . 
                         ?name ?hasStorage ?storage . 
                         ?storage ?hasMemory ?storageGB .
                         filter (?ramGB = ?ramLiteral) . 
                         filter (?storageGB = ?storageLiteral) .
                    """ + sparql_query_optional_part + """
                }}
                order by desc(?price)
                """
        
        init_bindings = create_init_bindings_for_sparql_query(self)
        init_bindings['type'] = RDF.type
        init_bindings['chipsetClass'] = chipset_class
        init_bindings['hasMemory'] = self.object_properties[constants.HAS_MEMORY]
        init_bindings['ramLiteral'] = ram_literal
        init_bindings['storageLiteral'] = storage_literal

        result = self.graph.query(query, initBindings = init_bindings)
        return get_list_of_phones_from_sparql_query(result)

    def get_phones_by_brand_os(self, brand, os):
        brand_individual = self.owl_manager.get_individual(brand)
        if not brand_individual:
            raise Exception("Error finding brand with name: " + brand)
        
        os_individual = self.owl_manager.get_individual(os)
        if not os_individual:
            raise Exception("Error finding OS with name: " + os)
        
        query = sparql_query_select_part + """
                where {{ ?name ?hasBrand ?brand . 
                         ?name ?hasOs  ?os .
                    """ + sparql_query_optional_part + """
                }}
                order by desc(?price)
                """
        
        init_bindings = create_init_bindings_for_sparql_query(self)
        init_bindings['brand'] = brand_individual
        init_bindings['os'] = os_individual

        result = self.graph.query(query, initBindings = init_bindings)
        return get_list_of_phones_from_sparql_query(result)

    def get_phone_with_best_camera_by_brand_date_price(self, brand, date, max_price):
        brand_individual = self.owl_manager.get_individual(brand)
        if not brand_individual:
            raise Exception("Error finding brand with name: " + brand)
        
        date_literal = Literal(date, datatype=XSD.dateTime)
        max_price_literal = Literal(max_price)

        query = sparql_query_select_part + """
                where {{ ?name ?hasBrand ?brand . 
                         ?name ?hasDate  ?date .
                         filter (?date >= ?minDate) .
                         ?name ?hasPrice ?price .
                         filter (?price <= ?maxPrice) .
                         ?name ?hasCamera ?camera .
                         ?camera ?hasMpx ?mpx .
                    """ + sparql_query_optional_part + """
                }}
                order by desc(?mpx) asc(?price)
                limit 1
                """

        init_bindings = create_init_bindings_for_sparql_query(self)
        init_bindings['brand'] = brand_individual
        init_bindings['minDate'] = date_literal
        init_bindings['maxPrice'] = max_price_literal
        init_bindings['hasMpx'] = self.object_properties[constants.HAS_MPX]

        result = self.graph.query(query, initBindings = init_bindings)
        return get_list_of_phones_from_sparql_query(result)

    def get_phones_by_screen_size_resolution(self, size, width, height):
        size_literal = Literal(size)
        width_literal = Literal(width)
        heigth_literal = Literal(height)

        query = sparql_query_select_part + """
                where {{ ?name ?hasScreenSize ?screen_dimension .
                         filter (?screen_dimension >= ?minSize) . 
                         ?name ?hasWidth  ?width .
                         filter (?width >= ?minWidth) .
                         ?name ?hasHeight ?height .
                         filter (?height >= ?minHeight) .
                    """ + sparql_query_optional_part + """
                }}
                order by desc(?screen_dimension)
                """
        
        init_bindings = create_init_bindings_for_sparql_query(self)
        init_bindings['minSize'] = size_literal
        init_bindings['minWidth'] = width_literal
        init_bindings['minHeight'] = heigth_literal

        result = self.graph.query(query, initBindings = init_bindings)
        return get_list_of_phones_from_sparql_query(result)
    
    def get_all_phones_with_camera(self, camera):
        mpx = Literal(camera, datatype = XSD.double)
        query = sparql_query_select_part + """
                where {{ ?name ?hasCamera ?camera . ?camera ?hasMpx ?mpx
                    """ + sparql_query_optional_part + """
                }}
                """

        init_bindings = create_init_bindings_for_sparql_query(self)
        init_bindings['mpx'] = mpx
        result = self.graph.query(query, initBindings = init_bindings)
        
        return get_list_of_phones_from_sparql_query(result)

    def get_all_phones_with_color(self, color):
        color_of_phone = Literal(color, datatype = XSD.string)
        query = sparql_query_select_part + """
                where {{ ?name ?hasColors ?colors .
                        FILTER(CONTAINS(LCASE(?colors), LCASE(?colorOfPhone)))
                    """ + sparql_query_optional_part + """ 
                }}
                """
        
        init_bindings = create_init_bindings_for_sparql_query(self)
        init_bindings['colorOfPhone'] = color_of_phone
        result = self.graph.query(query, initBindings = init_bindings)
        
        return get_list_of_phones_from_sparql_query(result)
    
    def get_color_for_specific_phone_model(self, model):
        model_of_phone = Literal(model, datatype=XSD.string)
        phone_uri = self.owl_manager.get_smart_phone_class(model_of_phone)
        
        if phone_uri is None :
            raise Exception("Error finding phone model with name: " + model)
        
        query =  """
                SELECT ?color
                    WHERE {{
                        ?phoneUri ?hasColors ?color .
                    }}
                """
        result = self.graph.query(query, initBindings = {
            'hasColors' : self.object_properties[constants.HAS_COLORS],
            'phoneUri' : phone_uri
        })
        
        colors = ([c for row in result for c in row['color'].split(',')])
        return colors
    
    def get_phone_with_min_price_for_brand(self, brand, oldest_date):
        oldest_date_for_phone = Literal(oldest_date, datatype=XSD.dateTime)
        brand_of_phone = self.owl_manager.get_individual(brand)
        if brand_of_phone is None :
            raise Exception("Error finding brand with name: " + brand)
        
        query = sparql_query_select_part + """
                where {{    ?name ?hasBrand ?brand . 
                            ?name ?hasDate ?date .
                            filter (?date >= ?oldestDate)
                    """ + sparql_query_optional_part + """
                }}
                order by asc(?price)
                """
        
        init_bindings = create_init_bindings_for_sparql_query(self)
        init_bindings['brand'] = brand_of_phone
        init_bindings['oldestDate'] = oldest_date_for_phone
        result = self.graph.query(query, initBindings = init_bindings)
        
        return get_list_of_phones_from_sparql_query(result)[0] if len(result) > 0 else None
    
    def get_phone_with_specified_camera_with_min_price_but_younger_than(self, oldest_date, mpx):
        oldest_date_for_phone = Literal(oldest_date, datatype=XSD.dateTime)
        mpx = Literal(mpx,datatype=XSD.double)
        query = sparql_query_select_part + """
                where {{ ?name ?hasCamera ?camera . 
                        ?camera ?hasMpx ?mpx .
                        ?name ?hasDate ?date .
                        filter (?date >= ?oldestDate)
                    """ + sparql_query_optional_part + """
                }}
                order by asc(?price)
                """
        
        init_bindings = create_init_bindings_for_sparql_query(self)
        init_bindings['mpx'] = mpx
        init_bindings['oldestDate'] = oldest_date_for_phone
        result = self.graph.query(query, initBindings = init_bindings)
        
        return get_list_of_phones_from_sparql_query(result)[0] if len(result) > 0 else None
    