from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import Funcionario, RegistroPonto, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/funcionarios/")
def criar_funcionario(nome: str, cargo: str, db: Session = next(get_db())):
    funcionario = Funcionario(nome=nome, cargo=cargo)
    db.add(funcionario)
    db.commit()
    db.refresh(funcionario)
    return funcionario


@app.post("/ponto/{funcionario_id}")
def registrar_ponto(funcionario_id: int, tipo: str, db: Session = next(get_db())):
    funcionario = db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    registro = RegistroPonto(funcionario_id=funcionario_id, tipo=tipo)
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro

@app.get("/funcionarios/{funcionario_id}")
def listar_funcionario(funcionario_id: int, db: Session = next(get_db())):
    funcionario = db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@app.get("/pontos/")
def listar_pontos(db: Session = next(get_db())):
    return db.query(RegistroPonto).all()