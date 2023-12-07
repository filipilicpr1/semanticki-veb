from rdflib import Graph, RDFS, RDF, XSD, URIRef, Literal
from Phone import Phone
import constants

class OWLManager:
    def __init__(self, file_name):
        self.graph = Graph()
        self.graph.parse(file_name)
        self.ontology_namespace = constants.ONTOLOGY_NAMESPACE
        self.named_individual = URIRef(constants.NAMED_INDIVIDUAL)
        self.object_properties = self.get_object_properties()
        self.smart_phones = self.get_smart_phones()

    def get_object_properties(self):
        object_properties = dict()

        for subj in self.graph.subjects():
            for key in constants.OBJECT_PROPERTIES:
                if key in subj and subj.split('#')[-1] in key and not key in object_properties:
                    object_properties[key] = subj
                    break
            
            if len(object_properties) == len(constants.OBJECT_PROPERTIES):
                break

        return object_properties
    
    def get_smart_phones(self):
        smart_phones = []

        for subj, obj in self.graph.subject_objects(predicate=RDFS.subClassOf):
            if self.ontology_namespace + constants.SMART_PHONE in obj:
                smart_phones.append(subj.split('#')[-1])
        
        return smart_phones
    
    def add_individual_phone(self, phone: Phone):
        try: 
            individual_name = URIRef(self.ontology_namespace + phone.name.replace(" ", "_"))

            class_name = self.get_smart_phone_class(phone.name)
            if not class_name:
                return
            
            self.graph.add((individual_name, RDF.type, self.named_individual))
            self.graph.add((individual_name, RDF.type, class_name))
            self.graph.add((individual_name, self.object_properties[constants.HAS_BRAND], self.get_individual(phone.brand)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_OS], self.get_individual(phone.os)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_CHIPSET], self.get_individual(phone.chipset)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_CAMERA], self.get_individual(phone.camera)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_STORAGE], self.get_individual(phone.storage)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_RAM], self.get_individual(phone.ram)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_SCREEN], self.get_individual(phone.screen)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_PRICE], Literal(phone.price)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_SCREEN_SIZE], Literal(phone.screen_dimension)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_WIDTH], Literal(phone.width)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_HEIGHT], Literal(phone.height)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_COLORS], Literal(phone.colors)))
            self.graph.add((individual_name, self.object_properties[constants.HAS_SALE_DATE], Literal(phone.date, datatype=XSD.dateTime)))
        except:
            raise ValueError("Error creating individual with name: " + phone.name)

    def get_smart_phone_class(self, name):
        for smart_phone in self.smart_phones:
            if smart_phone.replace("_", " ").lower() in name.lower():
                return URIRef(self.ontology_namespace + smart_phone)
            
        return None
    
    def get_chipset_class(self, chipset):
        name = chipset.strip().lower()
        for subj, obj in self.graph.subject_objects(predicate=RDFS.subClassOf):
            if name in subj.lower() and subj.lower().split('#')[-1] in name and constants.ONTOLOGY_NAMESPACE + constants.CHIPSET in obj:
                return subj

        return None

    def get_individual(self, name):
        name = name.lower().strip().replace(" ", "_")
        for subj, obj in self.graph.subject_objects(predicate=RDF.type):
            if name in subj and subj.split('#')[-1] in name and constants.NAMED_INDIVIDUAL in obj:
                return subj
            
        return None
    
    def save_ontology(self, file_name):
        with open(file_name, "w") as f:
            f.write(self.graph.serialize(format='pretty-xml'))