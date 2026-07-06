from backend import init_backend
from frontend import init_app

def main() -> None:
    backend = init_backend()
    app = init_app(backend)
    
    app.run()

if __name__ == "__main__":
    main()