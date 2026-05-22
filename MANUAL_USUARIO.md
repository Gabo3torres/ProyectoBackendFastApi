# Manual de Usuario — POS Backend

Sistema de Punto de Venta. Este manual explica cómo usar la aplicación desde el cliente web y desde la API directamente.

---

## 1. Requisitos previos

- Servidor corriendo en `http://127.0.0.1:8000` (ver README para arrancar)
- Navegador web moderno (Chrome, Firefox, Edge)
- Opcional: Postman para consumir la API directamente

---

## 2. Acceso al sistema

### 2.1 Desde el cliente web

1. Abrir el archivo `cliente_web/index.html` en el navegador
2. Ingresar email y contraseña
3. Hacer clic en **Ingresar**

> La primera vez que uses el sistema debes registrar un usuario desde Swagger (`/docs`) o Postman antes de poder iniciar sesión.

### 2.2 Desde Swagger (documentación interactiva)

1. Abrir `http://127.0.0.1:8000/docs` en el navegador
2. Usar el endpoint `POST /auth/login` para obtener el token
3. Hacer clic en el botón **Authorize** (arriba a la derecha)
4. Pegar el token con el formato: `Bearer <token>`
5. Confirmar con **Authorize**

A partir de ese momento todos los endpoints del Swagger estarán autenticados.

---

## 3. Roles de usuario

El sistema tiene dos niveles de acceso:

| Rol | Permisos |
|-----|----------|
| **admin** | Acceso total: crear, editar, eliminar productos y clientes, ver ventas |
| **cajero** | Puede consultar productos y clientes, registrar ventas. No puede crear ni eliminar productos |

---

## 4. Registro e inicio de sesión

### Registrar un usuario nuevo

**Endpoint:** `POST /auth/register`

```json
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan@tienda.com",
  "password": "micontraseña",
  "rol": "admin"
}
```

Valores válidos para `rol`: `"admin"` o `"cajero"`. Si se omite, queda como `"cajero"` por defecto.

### Iniciar sesión

**Endpoint:** `POST /auth/login`

```json
{
  "email": "juan@tienda.com",
  "password": "micontraseña"
}
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "access_token": "eyJhbGci...",
    "token_type": "bearer",
    "usuario": { "id": 1, "nombre": "Juan", "rol": "admin" }
  }
}
```

Guardar el `access_token` — se necesita en todos los endpoints siguientes.

---

## 5. Gestión de productos

### Ver todos los productos

**Endpoint:** `GET /productos/?page=1&limit=10`

Parámetros opcionales:
- `page`: número de página (por defecto: 1)
- `limit`: productos por página, máximo 100 (por defecto: 10)

### Crear un producto *(solo admin)*

**Endpoint:** `POST /productos/`

```json
{
  "nombre": "Café molido 500g",
  "descripcion": "Café premium colombiano",
  "precio": 12500,
  "stock": 50
}
```

- `nombre` y `precio` son obligatorios
- `stock` inicia en 0 si no se especifica
- `descripcion` es opcional

### Actualizar un producto *(solo admin)*

**Endpoint:** `PUT /productos/{id}`

Solo se envían los campos que se quieren cambiar:

```json
{
  "precio": 13500,
  "stock": 100
}
```

### Desactivar un producto *(solo admin)*

**Endpoint:** `DELETE /productos/{id}`

El producto no se borra de la base de datos — queda marcado como inactivo. El historial de ventas que lo incluye se conserva.

---

## 6. Gestión de clientes

### Ver todos los clientes

**Endpoint:** `GET /clientes/`

Devuelve la lista de clientes activos.

### Crear un cliente

**Endpoint:** `POST /clientes/`

```json
{
  "nombre": "María",
  "apellido": "García",
  "email": "maria@ejemplo.com",
  "telefono": "300-1234",
  "direccion": "Calle 10 #5-20"
}
```

- `nombre` y `apellido` son obligatorios
- Los demás campos son opcionales
- Si se proporciona email, debe ser único en el sistema

### Actualizar un cliente

**Endpoint:** `PUT /clientes/{id}`

```json
{
  "telefono": "310-9999",
  "direccion": "Carrera 5 #20-10"
}
```

Solo se envían los campos a modificar.

### Desactivar un cliente *(solo admin)*

**Endpoint:** `DELETE /clientes/{id}`

Al igual que los productos, el cliente no se elimina físicamente.

---

## 7. Registro de ventas

### Registrar una venta

**Endpoint:** `POST /ventas/`

```json
{
  "cliente_id": 3,
  "observacion": "Venta a crédito",
  "items": [
    { "producto_id": 1, "cantidad": 2 },
    { "producto_id": 4, "cantidad": 1 }
  ]
}
```

- `cliente_id` es opcional (venta de mostrador sin cliente registrado)
- `items` debe tener al menos un producto
- El sistema valida que haya stock suficiente antes de registrar
- El stock se descuenta automáticamente al confirmar la venta

**Errores posibles:**
| Código | Motivo |
|--------|--------|
| 400 | Lista de items vacía |
| 400 | Stock insuficiente para algún producto |
| 404 | Producto no existe o está inactivo |

### Ver historial de ventas

**Endpoint:** `GET /ventas/`

Devuelve todas las ventas ordenadas de más reciente a más antigua, con sus detalles completos.

### Ver detalle de una venta

**Endpoint:** `GET /ventas/{id}`

```json
{
  "data": {
    "id": 5,
    "total": 29000,
    "fecha": "2026-05-22T10:30:00",
    "detalles": [
      { "producto_id": 1, "cantidad": 2, "precio_unitario": 12500, "subtotal": 25000 },
      { "producto_id": 4, "cantidad": 1, "precio_unitario": 4000,  "subtotal": 4000 }
    ]
  }
}
```

---

## 8. Estructura de las respuestas

Todos los endpoints devuelven el mismo formato:

```json
{
  "success": true,
  "message": "Descripción del resultado",
  "data": { ... },
  "links": [
    { "rel": "self",   "href": "http://...", "method": "GET" },
    { "rel": "update", "href": "http://...", "method": "PUT" }
  ],
  "timestamp": "2026-05-22T10:30:00"
}
```

- `success`: `true` si la operación fue exitosa
- `data`: el objeto o lista resultado (puede ser `null`)
- `links`: acciones disponibles sobre el recurso (HATEOAS)
- `timestamp`: fecha y hora UTC de la respuesta

---

## 9. Códigos de error frecuentes

| Código | Significado | Solución |
|--------|-------------|----------|
| 400 | Datos inválidos o regla de negocio no cumplida | Revisar el campo `detail` de la respuesta |
| 401 | No autenticado o token inválido/expirado | Hacer login nuevamente para obtener un token nuevo |
| 403 | Autenticado pero sin permiso (rol insuficiente) | Usar una cuenta con rol `admin` |
| 404 | Recurso no encontrado | Verificar que el ID exista y esté activo |
| 422 | Formato de datos incorrecto | Revisar los tipos y campos obligatorios del request |

---

## 10. Autenticación alternativa con API Key

Como alternativa al JWT, se puede usar la API Key estática en el header:

```http
X-API-Key: mi-api-key-secreta-2026
```

Esto es útil para scripts o pruebas rápidas sin necesidad de hacer login.

---

## 11. Archivo de auditoría

Cada acción relevante queda registrada automáticamente en el archivo `audit.log` en la raíz del proyecto:

```
[2026-05-22 10:30:00] | CREAR      | productos    | usuario: admin@pos.com         | id=5 nombre='Café'
[2026-05-22 10:31:00] | VENTA      | ventas       | usuario: cajero@pos.com        | id=3 total=$29.000
[2026-05-22 10:32:00] | LOGIN_FAIL | usuarios     | usuario: desconocido@mail.com  | credenciales incorrectas
```

El archivo rota automáticamente cuando supera 1 MB, conservando los últimos 3 archivos históricos.
