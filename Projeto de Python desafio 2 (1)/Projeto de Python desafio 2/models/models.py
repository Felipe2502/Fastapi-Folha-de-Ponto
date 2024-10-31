from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cargo = Column(String)
    registros = relationship("RegistroPonto", back_populates="funcionario")


class RegistroPonto(Base):
    __tablename__ = 'registros_ponto'
    id = Column(Integer, primary_key=True, index=True)
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'))
    data_hora = Column(DateTime, default=datetime.utcnow)
    tipo = Column(String)  # "entrada" ou "saida"
    funcionario = relationship("Funcionario", back_populates="registros")