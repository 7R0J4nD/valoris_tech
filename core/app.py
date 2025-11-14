from fastapi import FastAPI
from core.setup import PROJECT_INFO
from core.extensions import configure_cors
from src.db.database import init_db
from src.routes import router as main_router  # router centralisé

def create_app() -> FastAPI:
    app = FastAPI(
        title=PROJECT_INFO["title"],
        description=PROJECT_INFO["description"],
        version=PROJECT_INFO["version"]
    )

    configure_cors(app)
    init_db()

    app.include_router(main_router)  # inclut tous les sous-routers

    return app
