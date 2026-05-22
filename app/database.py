# Configuración de la base de datos con SQLAlchemy.
# Define el motor de conexión, la sesión y la clase Base de la que heredan todos los modelos ORM.
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite guardado en un archivo local. En producción se reemplazaría por PostgreSQL/MySQL.
DATABASE_URL = "sqlite:///./tienda.db"

# check_same_thread=False es necesario para SQLite con FastAPI,
# ya que FastAPI puede manejar requests en hilos distintos al que creó la conexión.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal: fábrica de sesiones. autocommit=False significa que los cambios
# solo se guardan cuando se llama explícitamente a db.commit().
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase padre de todos los modelos ORM. SQLAlchemy la usa para conocer todas las tablas.
Base = declarative_base()


def get_db():
    # Generador de sesiones usado como dependencia en FastAPI (Depends(get_db)).
    # El bloque try/finally garantiza que la sesión se cierre aunque ocurra un error en el endpoint.
    db = SessionLocal()
    try:
        yield db  # Cede la sesión al endpoint; FastAPI la inyecta automáticamente.
    finally:
        db.close()
