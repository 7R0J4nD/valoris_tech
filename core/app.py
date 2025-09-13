
from fastapi import FastAPI
from core.setup import PROJECT_INFO
from core.extensions import configure_cors
from src.db.database import init_db
from src.routes import router
from src.websocket import ws_router


def create_app() -> FastAPI:
    """Initialise et retourne une instance de FastAPI."""

    app = FastAPI(
        title=PROJECT_INFO["title"],
        description=PROJECT_INFO["description"],
        version=PROJECT_INFO["version"]
    )

    configure_cors(app)  # Ajoute le middleware CORS
    init_db()  # Initialise la base de données

    app.include_router(router)  # Charge les routes API
    app.include_router(ws_router)  # Active WebSockets

    return app
