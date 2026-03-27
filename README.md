# CRM Backend - Sistema de Gestión Comercial

Este proyecto es un backend REST desarrollado en Flask que simula un sistema CRM para una empresa de venta de tecnología (tipo Global Hardware).

Permite gestionar clientes, productos, inventario, usuarios y ventas, incluyendo validaciones de negocio como control de stock.

---

## 🚀 Tecnologías utilizadas

* Python 3
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* PostgreSQL
* SQLAlchemy ORM

---

## 📦 Funcionalidades principales

### 👥 Clientes

* Crear cliente
* Listar clientes
* Obtener cliente por ID
* Actualizar cliente (PATCH)
* Baja lógica (DELETE → activo = false)
* Filtrar por activos/inactivos

---

### 📦 Productos

* Crear producto
* Listar productos
* Filtrar activos/inactivos
* Ver productos con stock bajo
* Actualizar producto (PATCH)
* Ajustar stock (`PATCH /productos/<id>/stock`)
* Baja lógica

---

### 🏷️ Categorías

* Crear categoría
* Listar categorías

---

### 👤 Usuarios

* Crear usuario
* Listar usuarios
* Obtener usuario
* Baja lógica

---

### 💰 Ventas

* Registrar venta
* Validación de cliente y usuario
* Validación de stock
* Descuento automático de inventario
* Creación de cabecera y detalle
* Listar ventas
* Obtener venta por ID
* Obtener ventas por cliente

---

## 🧠 Lógica de negocio implementada

* No se pueden vender productos inactivos
* No se puede vender sin stock suficiente
* No se pueden usar usuarios inactivos
* No se pueden duplicar emails en clientes/usuarios
* Baja lógica en lugar de eliminación física
* Operaciones transaccionales en ventas

---

## 📂 Estructura del proyecto

```
crm/
├── app/
│   ├── models/
│   ├── routes/
│   ├── extensions.py
│   ├── config.py
│   └── __init__.py
├── migrations/
├── run.py
├── requirements.txt
└── .env
```

---

## ⚙️ Instalación y ejecución

### 1. Clonar repositorio

```bash
git clone <repo>
cd crm
```

---

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4. Configurar base de datos

Crear base PostgreSQL:

```sql
CREATE DATABASE crm_db;
```

Configurar `.env`:

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/crm_db
```

---

### 5. Migraciones

```bash
flask --app run.py db init
flask --app run.py db migrate -m "init"
flask --app run.py db upgrade
```

---

### 6. Ejecutar servidor

```bash
python run.py
```

Servidor disponible en:

```
http://127.0.0.1:5000
```

---

## 📡 Ejemplos de uso

### Crear cliente

```bash
curl -X POST http://127.0.0.1:5000/clientes \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Joaquin","apellido":"Alzogaray","email":"joaquin@mail.com"}'
```

---

### Crear producto

```bash
curl -X POST http://127.0.0.1:5000/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre":"Monitor Samsung",
    "precio":150000,
    "costo":100000,
    "stock_actual":10,
    "stock_minimo":3,
    "categoria_id":1
  }'
```

---

### Registrar venta

```bash
curl -X POST http://127.0.0.1:5000/ventas \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "usuario_id": 1,
    "items": [
      {
        "producto_id": 1,
        "cantidad": 2
      }
    ]
  }'
```

---

### Ajustar stock

```bash
curl -X PATCH http://127.0.0.1:5000/productos/1/stock \
  -H "Content-Type: application/json" \
  -d '{"cantidad":5}'
```

---

## 🧪 Casos de error contemplados

* Stock insuficiente
* Producto inexistente
* Cliente inexistente
* Usuario inactivo
* Campos inválidos
* Duplicación de email

---

## 📈 Posibles mejoras futuras

* Autenticación (JWT)
* Roles y permisos
* Frontend (React/Vue)
* Dashboard de ventas
* Reportes
* Tests automatizados
* Deploy en la nube (Render)

---

## 👨‍💻 Autor

Proyecto desarrollado como práctica de backend orientado a sistemas empresariales (CRM/ERP).
