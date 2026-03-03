# Sistema Banco de Sangre (Web App)

Solucion integral para la gestion de un banco de sangre. Plataforma disenada para el registro y control de donantes, donaciones, inventario de sangre, solicitudes y transfusiones.

---

## Arquitectura de Software

El proyecto utiliza una Arquitectura Multicapa para separar responsabilidades y facilitar el escalamiento.

### Backend (FastAPI + PostgreSQL)
- Controllers: Manejan las peticiones HTTP y validan los roles de usuario.
- Services: Contienen la logica de negocio y las reglas de validacion.
- Models: Definen las entidades de la base de datos mediante SQLAlchemy.
- Schemas (DTOs): Definen la estructura de los datos (Pydantic).
- dbConfig: Centraliza la conexion y el ciclo de vida de las sesiones.

### Frontend (Vue.js 3 + Pinia + Vite)
- Vue Router: Navegacion entre vistas con guards de autenticacion.
- Pinia: Gestion de estado global (Sesion y Roles).
- Axios: Comunicacion con la API REST del backend.
- Responsive Design: Interfaz adaptada a multiples resoluciones.

---

## Estructura del Proyecto

```text
/banco-sangre
│
├── backend
│   ├── app
│   │   ├── dbConfig/               # Conexion y configuracion de DB
│   │   │   ├── databaseSession.py
│   │   │   └── baseModels.py
│   │   ├── controllers/            # Rutas divididas por modulo
│   │   │   ├── authController.py
│   │   │   ├── donantesController.py
│   │   │   ├── donacionesController.py
│   │   │   ├── inventarioController.py
│   │   │   ├── solicitudesController.py
│   │   │   └── transfusionesController.py
│   │   ├── models/                 # Modelos de datos (SQLAlchemy)
│   │   │   ├── usuarioModel.py
│   │   │   ├── donanteModel.py
│   │   │   ├── donacionModel.py
│   │   │   ├── inventarioModel.py
│   │   │   ├── solicitudModel.py
│   │   │   └── transfusionModel.py
│   │   ├── schemas/                # Validaciones Pydantic
│   │   │   ├── authSchema.py
│   │   │   ├── donanteSchema.py
│   │   │   ├── donacionSchema.py
│   │   │   ├── inventarioSchema.py
│   │   │   ├── solicitudSchema.py
│   │   │   └── transfusionSchema.py
│   │   ├── core/                   # Seguridad JWT y Hashing
│   │   │   ├── security.py
│   │   │   └── config.py
│   │   └── main.py                 # Punto de entrada de la API
│   ├── .env                        # Variables de entorno (Ignorado en Git)
│   └── requirements.txt            # Dependencias de Python
│
├── frontend
│   ├── public/                     # Archivos estaticos
│   ├── src
│   │   ├── views/                  # Vistas por modulo
│   │   │   ├── LoginView.vue
│   │   │   ├── DashboardView.vue
│   │   │   ├── DonantesView.vue
│   │   │   ├── DonacionesView.vue
│   │   │   ├── InventarioView.vue
│   │   │   ├── SolicitudesView.vue
│   │   │   └── TransfusionesView.vue
│   │   ├── components/             # Componentes reutilizables
│   │   │   └── AppLayout.vue
│   │   ├── apiServices/            # Clientes Axios por modulo
│   │   │   ├── authService.js
│   │   │   ├── donantesService.js
│   │   │   ├── donacionesService.js
│   │   │   ├── inventarioService.js
│   │   │   ├── solicitudesService.js
│   │   │   └── transfusionesService.js
│   │   ├── store/                  # Pinia: Auth
│   │   │   └── authStore.js
│   │   ├── router/                 # Vue Router con guards
│   │   │   └── index.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── certs/                          # Certificados SSL (Ignorado en Git)
├── .gitignore
└── README.md
```

---

## Base de Datos — 6 Tablas

| Tabla | Descripcion |
|-------|-------------|
| `usuarios` | Login con roles (admin, enfermero, medico) |
| `donantes` | Datos personales del donante |
| `donaciones` | Registro de cada donacion |
| `inventario_sangre` | Stock por tipo de sangre |
| `solicitudes` | Pedidos de sangre |
| `transfusiones` | Registro de entregas |

---

## Requisitos

- Python 3.11+
- Node.js 20+
- PostgreSQL (instalado localmente)
- Git for Windows (incluye OpenSSL para los certificados)

---

## Instrucciones de instalacion

Se iran agregando conforme avance el proyecto.