
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

def configure_cors(app):
    """Ajoute le middleware CORS à l'application FastAPI."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
