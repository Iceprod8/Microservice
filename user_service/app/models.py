from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    uid = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    preferences = relationship("UserPreference", back_populates="user")

class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"))
    id_genre = Column(Integer, nullable=False)  # Peut être un lien vers une table de genres
    user = relationship("User", back_populates="preferences")
