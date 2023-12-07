from abc import abstractmethod, ABC

class Command(ABC):
    def __init__(self, user_interface, sparql_manager) -> None:
        self.user_interface = user_interface
        self.sparql_manager = sparql_manager
        
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def description(self):
        pass