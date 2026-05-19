# Agora

Plataforma web de gestión de servicios y pedidos que conecta clientes con proveedores especializados, con notificaciones automáticas por correo en cada cambio de estado del pedido.

Proyecto académico — Laboratorio WSGI · Instituto Tecnológico Metropolitano (ITM)

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)
- [Requisitos previos](#requisitos-previos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Configuración de entorno](#configuración-de-entorno)
- [Modelos de datos](#modelos-de-datos)
- [Flujo de operaciones](#flujo-de-operaciones)
- [Equipo](#equipo)

---

## Descripción

Agora es una aplicación web multi-rol que gestiona el ciclo completo de un pedido de servicio: desde la solicitud del cliente hasta la facturación por parte del proveedor. Cada transición de estado dispara una notificación automática por correo electrónico al cliente.

El sistema soporta cuatro categorías de servicio, cada una con su propio proveedor y flujo operativo:

| Categoría         | Proveedor                          | Color de marca |
|-------------------|------------------------------------|----------------|
| Restaurante       | Comida a domicilio                 | `#FF4757`      |
| Servicios técnicos| Ferretería / técnicos del hogar    | `#FF6B35`      |
| Farmacia          | Medicamentos e insumos de salud    | `#00B894`      |
| Paquetería        | Empresa de envíos y mensajería     | `#5B7FFF`      |

---

## Características

**Panel del cliente**
- Catálogo de servicios filtrable por categoría
- Formulario de pedido con dirección y correo de contacto
- Historial de pedidos con línea de tiempo de estados
- Seguimiento en tiempo real del estado del envío
- Calificación del servicio al finalizar (estrellas y comentario)

**Panel del proveedor**
- Selector de perfil al ingresar (restaurante, técnico, farmacia, paquetería)
- Dashboard con KPIs del día y alertas de stock
- Gestión de pedidos entrantes: aceptar, rechazar, actualizar estado
- Control de inventario con alertas de stock mínimo
- Flujo de operaciones para farmacia y paquetería: picking, packing y facturación

**Notificaciones automáticas**
- Correo al cliente en cada transición de estado del pedido
- Correo al proveedor cuando el stock de un producto baja del mínimo definido

---

## Arquitectura

```
Cliente (navegador)
        |
        | HTTP
        v
   Flask / Gunicorn          <- servidor WSGI
        |
        |-- PostgreSQL        <- base de datos relacional
        |-- Redis             <- broker de mensajes
        |-- Celery Worker     <- tareas asíncronas (correos)
        |-- Gmail SMTP        <- envío de notificaciones
```

Todos los servicios se orquestan con Docker Compose.

---

## Estructura del proyecto

```
Proyecto/
├── index.html                  # Landing page
├── css/
│   └── styles.css              # Hoja de estilos global compartida
├── js/
│   ├── tema.js                 # Gestor de tema claro/oscuro (persistido en localStorage)
│   ├── login.js                # Lógica de autenticación y selección de rol
│   ├── picking.js              # Interacciones del flujo de picking
│   └── facturacion.js          # Interacciones del flujo de facturación
├── pages/
│   ├── login.html              # Inicio de sesión con selección de rol
│   ├── cliente.html            # Panel del cliente (catálogo, pedidos, seguimiento)
│   ├── proveedor.html          # Panel del proveedor (pedidos, inventario, operaciones)
│   ├── dashboard.html          # Dashboard de inventario avanzado
│   ├── picking.html            # Operación de picking
│   ├── packing.html            # Operación de packing
│   └── facturacion.html        # Operación de facturación y cierre
├── imagenes/
│   ├── logo/
│   │   ├── agoraN.png          # Logo tema claro
│   │   └── agoraO.png          # Logo tema oscuro
│   ├── comida.jpg
│   ├── electricista.jpg
│   ├── farmacia.jpg
│   └── paquetes.jpg
├── docker-compose.yml
└── README.md
```

---

## Tecnologías

### Frontend (implementado)

| Tecnología      | Uso                                              |
|-----------------|--------------------------------------------------|
| HTML5           | Estructura semántica de todas las vistas         |
| CSS3 puro       | Estilos globales, variables, modo oscuro, responsive |
| JavaScript vanilla | Lógica del cliente sin dependencias externas |
| Google Fonts    | Syne (títulos) y DM Sans (cuerpo)                |

### Backend (por implementar con el profesor)

| Tecnología    | Uso                                                |
|---------------|----------------------------------------------------|
| Python 3      | Lenguaje principal del servidor                    |
| Flask         | Framework web ligero                               |
| Gunicorn      | Servidor WSGI en producción                        |
| PostgreSQL    | Base de datos relacional                           |
| SQLAlchemy    | ORM para interacción con la base de datos          |
| Celery        | Cola de tareas para envío asíncrono de correos     |
| Redis         | Broker de mensajes para Celery                     |
| smtplib       | Envío de correos via Gmail SMTP                    |
| Docker Compose| Orquestación de todos los servicios                |

---

## Requisitos previos

Para ejecutar solo el frontend no se requiere ninguna dependencia adicional.

Para ejecutar el stack completo con Docker:

- [Docker](https://docs.docker.com/get-docker/) >= 24.x
- [Docker Compose](https://docs.docker.com/compose/install/) >= 2.x

---

## Instalación y ejecución

### Frontend (sin servidor)

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd Logica2026-1/Proyecto
   ```

2. Abrir `index.html` directamente en el navegador, o usar Live Server en VS Code:
   - Instalar la extensión **Live Server** en VS Code
   - Clic derecho sobre `index.html` > `Open with Live Server`
   - La aplicación quedará disponible en `http://127.0.0.1:5500`

### Stack completo con Docker

1. Configurar las variables de entorno (ver sección [Configuración de entorno](#configuración-de-entorno)).

2. Levantar todos los servicios:
   ```bash
   docker compose up --build
   ```

3. La aplicación estará disponible en `http://localhost:5000`.

4. Para detener los servicios:
   ```bash
   docker compose down
   ```

### Contenedores definidos en `docker-compose.yml`

| Servicio | Descripción                          |
|----------|--------------------------------------|
| `web`    | Aplicación Flask servida con Gunicorn|
| `db`     | Base de datos PostgreSQL             |
| `redis`  | Broker de mensajes para Celery       |
| `worker` | Celery worker para envío de correos  |

---

## Configuración de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos
DATABASE_URL=postgresql://usuario:contraseña@db:5432/agora

# Correo (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=agora.itm.grupo@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx

# Celery / Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Flask
FLASK_ENV=development
SECRET_KEY=cambiar-en-produccion
```

> El archivo `.env` no debe subirse al repositorio. Verificar que este listado en `.gitignore`.

---

## Modelos de datos

Esquema relacional planeado para la implementación del backend:

```
Usuario
  id, nombre, email, password_hash, rol (cliente | proveedor)

Proveedor
  id, nombre, categoria, usuario_id (FK), calificacion_promedio

Producto
  id, nombre, descripcion, precio, stock, stock_minimo, proveedor_id (FK), categoria

Pedido
  id, cliente_id (FK), proveedor_id (FK), estado, total, fecha_creacion

DetallePedido
  id, pedido_id (FK), producto_id (FK), cantidad, precio_unitario

Calificacion
  id, pedido_id (FK), cliente_id (FK), estrellas, comentario, fecha

Notificacion
  id, pedido_id (FK), destinatario_email, tipo_evento, fecha_envio
```

---

## Flujo de operaciones

### Estados del pedido y correos asociados

```
Pedido recibido       ->  Correo: "Tu solicitud fue confirmada"
        |
Proveedor asignado    ->  Correo: "Te asignamos un proveedor"
        |
En camino / servicio  ->  Correo: "Tu pedido va en camino"
        |
Entregado             ->  Correo: "Pedido entregado, califica tu experiencia"
        |
Calificado            ->  El cliente puntua con estrellas y comentario
```

### Flujo interno del proveedor (farmacia y paquetería)

```
Pedido aceptado
        |
     Picking          ->  El operario recolecta los productos del inventario
        |
     Packing          ->  Se empaca, se registra peso y se etiqueta
        |
  Facturacion         ->  Se emite la factura y se registra la salida del inventario
```

---

## Equipo

| Nombre       | Rol                        |
|--------------|----------------------------|
| Yesica       | Desarrollo frontend        |
| Daniel       | Desarrollo frontend        |
| Tomas        | Desarrollo frontend        |
| Juan Manuel  | Desarrollo frontend        |

Proyecto supervisado por el docente de la materia Logica de Programación — ITM, 2026.
