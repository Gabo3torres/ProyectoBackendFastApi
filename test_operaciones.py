# Script de prueba funcional de la API: crea productos, clientes y ventas mediante requests HTTP.
# Requiere que el servidor esté corriendo en http://127.0.0.1:8000 antes de ejecutarlo.
# Ejecutar con: python test_operaciones.py
import requests

BASE = "http://127.0.0.1:8000"

# Helpers para imprimir resultados con formato visual.
ok  = lambda msg: print(f"  [OK]   {msg}")
err = lambda msg: print(f"  [FAIL] {msg}")
sep = lambda t:   print(f"\n{'='*55}\n  {t}\n{'='*55}")


def main():
    # Contadores para el resumen final.
    resumen = {
        "productos_creados": 0,
        "clientes_creados": 0,
        "ventas_ok": 0,
        "ventas_fallidas_stock": 0,
    }

    # ── Login ────────────────────────────────────────────────
    sep("PREPARANDO SESIÓN")
    # Se intenta registrar el usuario (puede ya existir; se ignora el error).
    requests.post(f"{BASE}/auth/register", json={
        "nombre": "Admin", "apellido": "Test",
        "email": "admin_ops@mail.com", "password": "admin1234"
    })
    r = requests.post(f"{BASE}/auth/login", json={
        "email": "admin_ops@mail.com", "password": "admin1234"
    })
    if r.status_code != 200:
        print("  ERROR: no se pudo hacer login. ¿El servidor está corriendo?")
        return
    headers = {"Authorization": f"Bearer {r.json()['access_token']}"}
    ok("Login exitoso")

    # ── Crear productos ──────────────────────────────────────
    sep("PRUEBA — CREAR PRODUCTOS")
    productos = [
        {"nombre": "Café molido 500g",    "precio": 12500, "stock": 10},
        {"nombre": "Azúcar blanca 1kg",   "precio": 3500,  "stock": 5},
        {"nombre": "Leche entera 1L",     "precio": 4200,  "stock": 20},
        {"nombre": "Pan tajado 600g",     "precio": 6800,  "stock": 3},
        {"nombre": "Aceite vegetal 900ml","precio": 9100,  "stock": 0},  # sin stock, para probar validación
    ]
    ids_productos = []
    for p in productos:
        r = requests.post(f"{BASE}/productos/", json=p, headers=headers)
        if r.status_code == 201:
            ids_productos.append(r.json()["id"])
            resumen["productos_creados"] += 1
            ok(f"Producto creado: {p['nombre']}  (stock: {p['stock']})")
        else:
            err(f"Falló crear: {p['nombre']} — {r.json()}")

    # ── Crear clientes ───────────────────────────────────────
    sep("PRUEBA — CREAR CLIENTES")
    clientes = [
        {"nombre": "Laura",  "apellido": "Gómez",   "telefono": "300-1111"},
        {"nombre": "Carlos", "apellido": "Herrera",  "telefono": "301-2222"},
        {"nombre": "María",  "apellido": "Rodríguez","telefono": "302-3333"},
    ]
    ids_clientes = []
    for c in clientes:
        r = requests.post(f"{BASE}/clientes/", json=c, headers=headers)
        if r.status_code == 201:
            ids_clientes.append(r.json()["id"])
            resumen["clientes_creados"] += 1
            ok(f"Cliente creado: {c['nombre']} {c['apellido']}")
        else:
            err(f"Falló crear: {c['nombre']} — {r.json()}")

    # ── Ventas exitosas ──────────────────────────────────────
    sep("PRUEBA — VENTAS EXITOSAS")
    ventas_ok = [
        {
            "desc": "Venta 1: café + azúcar (cliente 1)",
            "payload": {
                "cliente_id": ids_clientes[0] if ids_clientes else None,
                "items": [
                    {"producto_id": ids_productos[0], "cantidad": 2},
                    {"producto_id": ids_productos[1], "cantidad": 1},
                ]
            }
        },
        {
            "desc": "Venta 2: leche + pan (cliente 2)",
            "payload": {
                "cliente_id": ids_clientes[1] if len(ids_clientes) > 1 else None,
                "items": [
                    {"producto_id": ids_productos[2], "cantidad": 3},
                    {"producto_id": ids_productos[3], "cantidad": 1},
                ]
            }
        },
        {
            "desc": "Venta 3: sin cliente (mostrador)",
            "payload": {
                "items": [
                    {"producto_id": ids_productos[0], "cantidad": 1},
                ]
            }
        },
    ]
    for v in ventas_ok:
        r = requests.post(f"{BASE}/ventas/", json=v["payload"], headers=headers)
        if r.status_code == 201:
            resumen["ventas_ok"] += 1
            total = r.json()["total"]
            ok(f"{v['desc']}  →  Total: ${total:,.0f}")
        else:
            err(f"{v['desc']}  →  {r.json()['detail']}")

    # ── Venta fallida por stock insuficiente ─────────────────
    sep("PRUEBA — VALIDACIÓN DE STOCK (debe fallar)")
    venta_sin_stock = {
        "desc": "Venta con producto sin stock (aceite)",
        "payload": {
            "items": [{"producto_id": ids_productos[4], "cantidad": 5}]
        }
    }
    r = requests.post(f"{BASE}/ventas/", json=venta_sin_stock["payload"], headers=headers)
    if r.status_code == 400:
        resumen["ventas_fallidas_stock"] += 1
        ok(f"Validación funcionó correctamente → {r.json()['detail']}")
    else:
        err(f"Se esperaba error 400 pero llegó {r.status_code}")

    # ── Resumen final ────────────────────────────────────────
    sep("RESUMEN DE OPERACIONES")
    print(f"  Productos creados            : {resumen['productos_creados']}")
    print(f"  Clientes creados             : {resumen['clientes_creados']}")
    print(f"  Ventas registradas (exitosas): {resumen['ventas_ok']}")
    print(f"  Ventas rechazadas (stock)    : {resumen['ventas_fallidas_stock']}")
    print()


if __name__ == "__main__":
    main()
