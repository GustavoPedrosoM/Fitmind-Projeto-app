from sqlalchemy import Column, Integer, String
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
