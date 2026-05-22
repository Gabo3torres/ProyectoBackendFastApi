# Script de prueba de rendimiento: mide los tiempos de respuesta de los endpoints principales.
# Ejecuta cada llamada REPETICIONES veces y calcula promedio, mínimo y máximo en milisegundos.
# Requiere que el servidor esté corriendo en http://127.0.0.1:8000 antes de ejecutarlo.
# Ejecutar con: python test_performance.py
import requests
import time

BASE = "http://127.0.0.1:8000"
REPETICIONES = 5  # Cuántas veces se mide cada endpoint para obtener un promedio estable.


def medir(label, fn):
    # Ejecuta la función fn REPETICIONES veces midiendo el tiempo de cada llamada.
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()  # perf_counter tiene mayor precisión que time.time().
        resp = fn()
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1000)  # Convierte a milisegundos.
    promedio = sum(tiempos) / len(tiempos)
    minimo = min(tiempos)
    maximo = max(tiempos)
    estado = resp.status_code
    print(f"  {label}")
    print(f"    Status : {estado}")
    print(f"    Promedio: {promedio:.1f} ms  |  Min: {minimo:.1f} ms  |  Max: {maximo:.1f} ms")
    print()
    return resp


def main():
    print("=" * 55)
    print("  PRUEBA DE TIEMPOS DE RESPUESTA — POS API")
    print("=" * 55)
    print()

    # --- 1. Registrar usuario de prueba (ignora error si ya existe) ---
    print("[ Preparando usuario de prueba ]")
    requests.post(f"{BASE}/auth/register", json={
        "nombre": "Test",
        "apellido": "Performance",
        "email": "test_perf@mail.com",
        "password": "test1234"
    })

    # --- 2. Login y obtener token JWT ---
    resp_login = requests.post(f"{BASE}/auth/login", json={
        "email": "test_perf@mail.com",
        "password": "test1234"
    })

    if resp_login.status_code != 200:
        print("  ERROR: No se pudo hacer login. ¿El servidor está corriendo?")
        return

    token = resp_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("  Login OK — token obtenido")
    print()

    # --- Prueba 1: GET /productos/ — consulta paginada ---
    print("[ Prueba 1 — GET /productos/ ]")
    medir("GET /productos/", lambda: requests.get(f"{BASE}/productos/", headers=headers))

    # --- Prueba 2: POST /productos/ — creación de un producto ---
    print("[ Prueba 2 — POST /productos/ ]")
    payload_producto = {
        "nombre": "Producto Test",
        "descripcion": "Creado por test de performance",
        "precio": 9999,
        "stock": 100
    }
    ultimo_producto = None  # Guarda el último producto creado para usarlo en la prueba de venta.

    def crear_producto():
        nonlocal ultimo_producto
        r = requests.post(f"{BASE}/productos/", json=payload_producto, headers=headers)
        if r.status_code == 201:
            ultimo_producto = r.json()
        return r

    medir("POST /productos/", crear_producto)

    # --- Prueba 3: POST /ventas/ — proceso completo de venta ---
    print("[ Prueba 3 — POST /ventas/ ]")
    if ultimo_producto:
        payload_venta = {
            "observacion": "Venta de prueba performance",
            "items": [{"producto_id": ultimo_producto["id"], "cantidad": 1}]
        }
        medir("POST /ventas/", lambda: requests.post(f"{BASE}/ventas/", json=payload_venta, headers=headers))
    else:
        print("  SKIP: no se pudo crear producto, omitiendo prueba de venta")
        print()

    print("=" * 55)
    print("  Pruebas completadas")
    print("=" * 55)


if __name__ == "__main__":
    main()
