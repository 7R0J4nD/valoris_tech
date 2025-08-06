from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base
from passlib.context import CryptContext

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")

    def verify_password(self, plain_password: str) -> bool:
        """Vérifie si le mot de passe correspond au hash stocké."""
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash un mot de passe avant de le stocker."""
        return pwd_context.hash(password)
