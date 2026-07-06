from backend import Backend

class App:
    def __init__(self, backend: Backend) -> None:
        self.__backend = backend

    def run(self) -> None:
        print("App is running with backend:", self.__backend)