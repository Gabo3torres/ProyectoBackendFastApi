# ProyectoBackendFastApi

Un backend desarrollado con **FastAPI** que proporciona una API REST robusta y eficiente.

## 🚀 Características

- **Framework moderno**: Construido con FastAPI para máximo rendimiento
- **Documentación automática**: Swagger UI y ReDoc incluidos
- **Validación de datos**: Utiliza Pydantic para validación automática
- **API RESTful**: Endpoints bien estructurados y documentados
- **Código limpio**: Arquitectura escalable y mantenible

## 📋 Requisitos previos

- Python 3.8+
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/Gabo3torres/ProyectoBackendFastApi.git
   cd ProyectoBackendFastApi
   ```

2. **Crea un entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual**
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Uso

Ejecuta el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

## 📁 Estructura del proyecto

```
ProyectoBackendFastApi/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── app/
│   ├── __init__.py
│   ├── models/            # Modelos de datos (Pydantic)
│   ├── routes/            # Rutas/endpoints de la API
│   └── services/          # Lógica de negocio
└── README.md              # Este archivo
```

## 🔌 Endpoints principales

Aquí van los principales endpoints de tu API:

```
GET    /api/resource       - Obtener listado de recursos
POST   /api/resource       - Crear nuevo recurso
GET    /api/resource/{id}  - Obtener recurso específico
PUT    /api/resource/{id}  - Actualizar recurso
DELETE /api/resource/{id}  - Eliminar recurso
```

*Personaliza estos endpoints según tu proyecto*

## 📦 Dependencias principales

- **FastAPI** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validación de datos
- *[Agrega otras dependencias según tu proyecto]*

## 🧪 Testing

```bash
pytest
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, abre un issue primero para discutir los cambios propuestos.

## 📄 Licencia

Este proyecto está bajo la licencia MIT - ver el archivo LICENSE para más detalles.

## 👤 Autor

**Gabo3torres**
- GitHub: [@Gabo3torres](https://github.com/Gabo3torres)

## 📞 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

⭐ Si te fue útil, considera darle una estrella al repositorio.
