# Script de práctica de SQLAlchemy con interfaz de consola (sin FastAPI).
# Demuestra el ciclo completo: definir modelo → crear tabla → CRUD desde un menú interactivo.
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker

# Base de datos SQLite de práctica; separada de la BD principal de la app (tienda.db).
engine = create_engine('sqlite:///mi_base.db', echo=False)

Base = declarative_base()


# Modelo de práctica equivalente al Usuario de la app principal pero simplificado.
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    email = Column(String(100))
    fecha_registro = Column(DateTime, default=datetime.now)


# Crea la tabla si no existe al ejecutar el script.
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Menú interactivo en bucle infinito; se sale con la opción "3".
while True:
    print("1. Agregar usuario")
    print("2. Listar usuarios")
    print("3. Salir")
    opcion = input("Seleccione una opción: ")
    if opcion == '1':
        nombre = input("Ingrese el nombre: ")
        apellido = input("Ingrese el apellido: ")
        email = input("Ingrese el email: ")
        nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, email=email)
        session.add(nuevo_usuario)
        session.commit()
        print("Usuario agregado exitosamente.")

    elif opcion == '2':
        usuarios = session.query(Usuario).all()
        for usuario in usuarios:
            print(f"{usuario.id}: {usuario.nombre} {usuario.apellido} - {usuario.email} - {usuario.fecha_registro}")

    elif opcion == '3':
        print("Saliendo...")
        break

    else:
        print("Opción no válida. Intente nuevamente.")

session.close()
