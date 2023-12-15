from utilities.Phone import MobilePhone
import constants

sparql_query_select_part = """select ?name ?brand ?camera ?ram ?chipset ?os ?screen ?storage ?price ?date ?colors ?width ?height ?screen_dimension"""

sparql_query_optional_part =  """OPTIONAL {
                    ?name ?hasRam ?ram . 
                    ?name ?hasChipset ?chipset .
                    ?name ?hasBrand ?brand .
                    ?name ?hasOs ?os .
                    ?name ?hasScreen ?screen .
                    ?name ?hasStorage ?storage .
                    ?name ?hasPrice ?price .
                    ?name ?hasDate ?date .
                    ?name ?hasColors ?colors .
                    ?name ?hasWidth ?width .
                    ?name ?hasHeight ?height .
                    ?name ?hasScreenSize ?screen_dimension .
                    ?name ?hasCamera ?camera
                    }"""
                    
def create_init_bindings_for_sparql_query(graph) :
    init_bindings={
            'hasCamera' : graph.object_properties[constants.HAS_CAMERA], 
            'hasMpx' : graph.object_properties[constants.HAS_MPX], 
            'hasRam' : graph.object_properties[constants.HAS_RAM],
            'hasOs' : graph.object_properties[constants.HAS_OS],
            'hasBrand' : graph.object_properties[constants.HAS_BRAND],
            'hasScreen' : graph.object_properties[constants.HAS_SCREEN],
            'hasStorage' : graph.object_properties[constants.HAS_STORAGE],
            'hasPrice' : graph.object_properties[constants.HAS_PRICE],
            'hasDate' : graph.object_properties[constants.HAS_SALE_DATE],
            'hasColors' : graph.object_properties[constants.HAS_COLORS],
            'hasWidth' : graph.object_properties[constants.HAS_WIDTH],
            'hasHeight' : graph.object_properties[constants.HAS_HEIGHT],
            'hasScreenSize' : graph.object_properties[constants.HAS_SCREEN_SIZE],
            'hasChipset' : graph.object_properties[constants.HAS_CHIPSET]}
    
    return init_bindings
    
def get_list_of_phones_from_sparql_query(result) : 
    phones = []
    for row in result:
        name = row['name'].split('#')[-1]
        brand = row['brand'].split('#')[-1]
        camera_mpx = row['camera'].split('#')[-1]
        ram = row['ram'].split('#')[-1]
        chipset = row['chipset'].split('#')[-1]
        os = row['os'].split('#')[-1]
        screen = row['screen'].split('#')[-1]
        storage = row['storage'].split('#')[-1]
        price = row['price']
        date = row['date']
        colors = row['colors']
        width = row['width']
        height = row['height']
        screen_dimension = row['screen_dimension']
        
        phone = MobilePhone(name, brand, camera_mpx, chipset, os, ram, screen, storage, screen_dimension, width, height, date, price, colors)
        phones.append(phone)
    
    return phones