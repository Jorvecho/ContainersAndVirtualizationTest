from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import sys
from typing import List
import logging

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        logging.error(f"La variable de entorno '{var_name}' no está definida.")
        sys.exit(1)


DATABASE_URL = get_env_variable('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class EstudianteDB(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    edad = Column(Integer, nullable=False)

app = FastAPI(title="CRUD API", version="1.0.0")

class EstudianteCreate(BaseModel):
    nombre: str = Field(..., min_length=3, description="Nombre de usuario (mínimo 3 caracteres)")
    email: str = Field(..., description="Email del usuario")
    edad: int = Field(..., gt=0, description="Edad del usuario (debe ser un número positivo)")

class EstudianteResponse(BaseModel):
    id: int
    nombre: str
    email: str
    edad: int

def to_response(estudiante: EstudianteDB) -> EstudianteResponse:
    return EstudianteResponse(
        id=estudiante.id,
        nombre=estudiante.nombre,
        email=estudiante.email,
        edad=estudiante.edad
    )

Base.metadata.create_all(bind=engine)

@app.get("/estudiantes", response_model=List[EstudianteResponse])
def listar_estudiantes():
    """Lista todas las entidades"""
    with SessionLocal() as db:
        try:
            estudiantes = db.query(EstudianteDB).all()
        except SQLAlchemyError:
            logger.exception("Error de base de datos al listar estudiantes")
            raise HTTPException(status_code=500, detail="Error interno de base de datos")
        logger.info("Listando todos los estudiantes")
        return [to_response(estudiante) for estudiante in estudiantes]

@app.get("/estudiantes/{estudiante_id}", response_model=EstudianteResponse)
def obtener_estudiante(estudiante_id: int):
    """Recupera una entidad específica"""
    with SessionLocal() as db:
        try:
            estudiante = db.query(EstudianteDB).filter(EstudianteDB.id == estudiante_id).first()
        except SQLAlchemyError:
            logger.exception(f"Error de base de datos al obtener el estudiante {estudiante_id}")
            raise HTTPException(status_code=500, detail="Error interno de base de datos")
        if not estudiante:
            logger.warning(f"Estudiante con ID {estudiante_id} no encontrado")
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        logger.info(f"Estudiante obtenido con ID: {estudiante.id}")
        return to_response(estudiante)

@app.post("/estudiantes", response_model=EstudianteResponse, status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: EstudianteCreate):
    """Crea una nueva entidad"""
    with SessionLocal() as db:
        nuevo_estudiante = EstudianteDB(
            nombre=estudiante.nombre,
            email=estudiante.email,
            edad=estudiante.edad
        )
        try:
            db.add(nuevo_estudiante)
            db.commit()
            db.refresh(nuevo_estudiante)
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Error de base de datos al crear el estudiante")
            raise HTTPException(status_code=500, detail="Error interno de base de datos")
        logger.info(f"Estudiante creado con ID: {nuevo_estudiante.id}")
        return to_response(nuevo_estudiante)

@app.delete("/estudiantes/{estudiante_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(estudiante_id: int):
    """Borra una entidad"""
    with SessionLocal() as db:
        try:
            estudiante = db.query(EstudianteDB).filter(EstudianteDB.id == estudiante_id).first()
            if not estudiante:
                logger.warning(f"Estudiante con ID {estudiante_id} no encontrado")
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")
            db.delete(estudiante)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            logger.exception(f"Error de base de datos al eliminar el estudiante {estudiante_id}")
            raise HTTPException(status_code=500, detail="Error interno de base de datos")
        logger.info(f"Estudiante eliminado con ID: {estudiante_id}")

@app.get("/")
def root():
    return {"message": "CRUD API"}
