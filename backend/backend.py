from .model import ModelRegistry
from .controller import Controller

class Backend:
    def __init__(self, db_name: str, model_registry: ModelRegistry) -> None:
        self._model_registry = model_registry
        self._db_name = db_name
        self.__set_attributes__()

    def __set_attributes__(self) -> None:
        for model_name, model_class in self._model_registry._registry.items():
            attribute_name = model_name + "Controller"
            controller_instance = Controller(db_name=self._db_name, model=model_class)
            setattr(self, attribute_name, controller_instance)

    def __str__(self) -> str:
        return f"Backend(db_name={self._db_name}, model_registry={self._model_registry})"