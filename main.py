# Script de arranque del servidor de desarrollo.
# Ejecutar con: python main.py
# Uvicorn levanta la app FastAPI en http://0.0.0.0:8000 con recarga automática al editar archivos.
import uvicorn

if __name__ == "__main__":
    # "app.main:app" indica: módulo app/main.py → objeto FastAPI llamado "app".
    # reload=True reinicia el servidor automáticamente cuando se detectan cambios en el código.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
