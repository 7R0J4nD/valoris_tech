import uvicorn
from core.app import create_app  # Import de l’application initialisée

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5500, reload=True)
