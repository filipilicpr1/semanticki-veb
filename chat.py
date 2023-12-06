from OWLManager import OWLManager
from SPARQLManager import SPARQLManager
from UIHandler import UIHandler

owl_manager = OWLManager("GoodRelationsPopulated.owl")
sparql_manager = SPARQLManager(owl_manager)
ui_handler = UIHandler(sparql_manager)
ui_handler.run()