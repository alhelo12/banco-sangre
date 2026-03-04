# Sistema Banco de Sangre (Web App)

Solucion integral para la gestion de un banco de sangre. Plataforma disenada para el registro y control de donantes, donaciones, inventario de sangre, solicitudes y transfusiones.

---

## Arquitectura de Software

El proyecto utiliza una Arquitectura Multicapa para separar responsabilidades y facilitar el escalamiento.

### Backend (FastAPI + PostgreSQL)
- Controllers: Manejan las peticiones HTTP y validan los roles de usuario.
- Models: Definen las entidades de la base de datos mediante SQLAlchemy.
- Schemas (DTOs): Definen la estructura de los datos (Pydantic).
- dbConfig: Centraliza la conexion y el ciclo de vida de las sesiones.
- core: Seguridad JWT y hashing de contrasenas.

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
│   ├── docs/                       # Documentacion de la BD
│   │   ├── banco_sangre.sql        # Schema SQL
│   │   └── README.md               # Relaciones entre tablas
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
│   │   ├── apiServices/            # Clientes Axios
│   │   │   └── authService.js
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

---

## Instrucciones de instalacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/banco-sangre.git
cd banco-sangre
```

### 2. Crear la base de datos en PostgreSQL

```powershell
psql -U postgres -c "CREATE DATABASE banco_sangre;"
psql -U postgres -d banco_sangre -f backend/docs/banco_sangre.sql
```

> Si usas pgAdmin puedes abrir el archivo `backend/docs/banco_sangre.sql` y ejecutarlo directamente desde el Query Tool.
>
> Nota: Si al ejecutar el .sql ocurre algun error, no te preocupes. Al arrancar el servidor FastAPI creara las tablas automaticamente gracias a SQLAlchemy.

### 3. Configurar el Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Edita el archivo `.env` con tus credenciales:

```
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/banco_sangre
SECRET_KEY=una_clave_segura_de_al_menos_32_caracteres
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Arranca el servidor:

```powershell
uvicorn app.main:app --reload --port 8000
```

### 4. Configurar el Frontend

Abre una nueva terminal:

```powershell
cd frontend
npm install
npm run dev
```

---

## URLs

| Servicio | URL |
|----------|-----|
| App | http://localhost:5173 |
| API Docs (Swagger) | http://localhost:8000/api/docs |

---

## Flujo de uso

```
1. Registrar un usuario en /api/docs → POST /api/auth/register
2. Iniciar sesion en http://localhost:5173
3. Crear un donante
4. Registrar una donacion y cambiarla a "aprobada"
5. Agregar la unidad al inventario
6. Crear una solicitud y cambiarla a "aprobada"
7. Registrar la transfusion con el ID de la solicitud y del inventario
8. La solicitud cambia a "entregada" y el inventario a "usado" automaticamente
```