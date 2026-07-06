from .app import App

def init_app(backend) -> App:
    return App(backend)