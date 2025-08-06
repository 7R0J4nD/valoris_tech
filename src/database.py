
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings
import logging

# Configuration du logger pour capturer les erreurs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

# Création de l'engine pour PostgreSQL avec gestion des erreurs
try:
    engine = create_engine(settings.DB_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Connexion à PostgreSQL établie avec succès.")
except Exception as e:
    logger.error(f"Échec de la connexion à la base de données : {e}")
    engine = None  # Permet de signaler un problème avec la base

def init_db():
    """Initialise la base de données en créant les tables si elles n'existent pas."""
    if engine:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Tables de la base de données créées avec succès.")
        except Exception as error:
            logger.error(f"Erreur lors de l'initialisation des tables : {str(error)}")
    else:
        logger.error("Impossible d'initialiser la base de données car l'engine est indisponible.")


