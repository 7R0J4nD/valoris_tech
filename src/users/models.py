import enum

from sqlalchemy import Column, Integer, String, Boolean, Enum
from src.db.database import Base
from passlib.context import CryptContext

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(80), unique=False, nullable=True)
    lastname = Column(String(50), unique=False, nullable=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(25), unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)

    def verify_password(self, plain_password: str) -> bool:
        """Vérifie si le mot de passe correspond au hash stocké."""
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash un mot de passe avant de le stocker."""
        return pwd_context.hash(password)

