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
│   │   │   ├── usuariosController.py
│   │   │   ├── donantesController.py
│   │   │   ├── donacionesController.py
│   │   │   ├── inventarioController.py
│   │   │   ├── solicitudesController.py
│   │   │   ├── transfusionesController.py
│   │   │   └── configuracionRolesController.py
│   │   ├── models/                 # Modelos de datos (SQLAlchemy)
│   │   │   ├── usuarioModel.py
│   │   │   ├── donanteModel.py
│   │   │   ├── donacionModel.py
│   │   │   ├── inventarioModel.py
│   │   │   ├── solicitudModel.py
│   │   │   ├── transfusionModel.py
│   │   │   └── configuracionRolModel.py
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
│   ├── run.py                      # Arranque con SSL (solo desarrollo local)
│   ├── .env                        # Variables de entorno (Ignorado en Git)
│   └── requirements.txt            # Dependencias de Python
│
├── frontend
│   ├── public/                     # Archivos estaticos
│   ├── src
│   │   ├── views/                  # Vistas por modulo
│   │   │   ├── LoginView.vue
│   │   │   ├── DashboardView.vue
│   │   │   ├── ConfiguracionRolesView.vue
│   │   │   ├── UsuariosView.vue
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
│   └── README.md                   # Instrucciones para generar certificados
├── .gitignore
└── README.md
```

---

## Base de Datos — 7 Tablas

| Tabla | Descripcion |
|-------|-------------|
| `usuarios` | Login con roles (admin, enfermero, medico) |
| `donantes` | Datos personales del donante |
| `donaciones` | Registro de cada donacion |
| `inventario_sangre` | Stock por tipo de sangre |
| `solicitudes` | Pedidos de sangre |
| `transfusiones` | Registro de entregas |
| `configuracion_roles` | Prefijos de matricula para registro automatico de roles |

---

## Requisitos (desarrollo local)

- Python 3.11+
- Node.js 20+
- PostgreSQL (instalado localmente)
- OpenSSL (para generar certificados SSL)

---

## Instalacion local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/banco-sangre.git
cd banco-sangre
```

### 2. Generar certificados SSL

```powershell
# Windows
$env:OPENSSL_CONF = "C:\Program Files\OpenSSL-Win64\bin\openssl.cfg"
& "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
```

```bash
# Linux / Mac
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
```

> Ver instrucciones completas en `certs/README.md`.

### 3. Crear la base de datos en PostgreSQL

```powershell
psql -U postgres -c "CREATE DATABASE banco_sangre;"
psql -U postgres -d banco_sangre -f backend/docs/banco_sangre.sql
```

> Si usas pgAdmin puedes abrir `backend/docs/banco_sangre.sql` y ejecutarlo desde el Query Tool.
>
> Nota: Si al ejecutar el .sql ocurre algun error no te preocupes. Al arrancar el servidor FastAPI creara las tablas automaticamente gracias a SQLAlchemy.

### 4. Configurar el Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Crea el archivo `.env` con tus credenciales:

```
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/banco_sangre
SECRET_KEY=una_clave_segura_de_al_menos_32_caracteres
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Arranca el servidor con SSL:

```powershell
python run.py
```

> El servidor estara disponible en `https://localhost:8000`

### 5. Configurar el Frontend

Abre una nueva terminal:

```powershell
cd frontend
npm install
npm run dev
```

### URLs locales

| Servicio | URL |
|----------|-----|
| App | https://localhost:5173 |
| API Docs (Swagger) | https://localhost:8000/api/docs |

> El navegador mostrara una advertencia por el certificado autofirmado.
> Haz click en "Avanzado" → "Continuar de todas formas" para acceder.

---

## Despliegue en Railway (produccion)

[Railway](https://railway.app) permite desplegar backend, frontend y base de datos
de forma gratuita conectando directamente el repositorio de GitHub.
Railway provee HTTPS automatico con Let's Encrypt, no necesitas configurar SSL manualmente.

### Paso 1 — Crear cuenta y proyecto

1. Ve a https://railway.app y registrate con tu cuenta de GitHub
2. Click en `New Project` → `Deploy from GitHub repo` → selecciona `banco-sangre`

### Paso 2 — Agregar PostgreSQL

Dentro del proyecto click en `Add Service` → `Database` → `PostgreSQL`.

### Paso 3 — Configurar el Backend

Click en el servicio del backend → `Settings`:

**Build & Deploy:**
```
Root Directory:  backend
Start Command:   uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Variables:**
```
DATABASE_URL             ${{Postgres.DATABASE_URL}}
SECRET_KEY               una_clave_segura_de_al_menos_32_caracteres
ACCESS_TOKEN_EXPIRE_MINUTES  60
```

> Usar `${{Postgres.DATABASE_URL}}` conecta el backend directamente al servicio de Postgres del proyecto sin exponer credenciales.

### Paso 4 — Configurar el Frontend

Click en `Add Service` → `GitHub Repo` → selecciona el mismo repo.

**Build & Deploy:**
```
Root Directory:  frontend
Build Command:   npm run build
Start Command:   npx serve dist
```

**Variables:**
```
VITE_API_URL   https://TU-BACKEND.up.railway.app
```

> Reemplaza `TU-BACKEND` con el dominio generado por Railway para el backend.
> Lo encuentras en backend → `Settings` → `Networking` → `Generate Domain`.

### Paso 5 — Insertar datos iniciales

Las tablas se crean automaticamente al arrancar el backend. Solo falta insertar
los datos iniciales. Conectate a la BD desde pgAdmin usando las credenciales de
`Postgres → Connect → Public Network` y ejecuta:

```sql
INSERT INTO usuarios (nombre, email, password, rol) VALUES
('Administrador', 'admin@bancosangre.com', '$2b$12$uBswjFcA9WnAfeTwRamqqOiOuXu7nmTAwYlNd3xS.NU4qCag/DfVe', 'admin');

INSERT INTO configuracion_roles (prefijo, rol, descripcion) VALUES
('MED', 'medico', 'Personal medico'),
('ENF', 'enfermero', 'Personal de enfermeria');
```

### Paso 6 — Compartir la app

El link publico de la app lo encuentras en:
**banco-sangre\frontend → Settings → Networking → Domain**

---

## Flujo de uso

```
1. Iniciar sesion con el admin predefinido:
   Email: admin@bancosangre.com / Password: admin123
2. Ir a Configuracion y verificar o agregar prefijos de matricula
3. El personal se registra en la pantalla de registro con su matricula
   → el sistema asigna el rol automaticamente segun el prefijo
4. Crear un donante
5. Registrar una donacion y cambiarla a "aprobada"
6. Agregar la unidad al inventario
7. Crear una solicitud y cambiarla a "aprobada"
8. Registrar la transfusion con el ID de la solicitud y del inventario
9. La solicitud cambia a "entregada" y el inventario a "usado" automaticamente
```

---

## Roles y permisos

| Vista            | Admin | Enfermero | Medico |
|------------------|-------|-----------|--------|
| Dashboard        | ✅    | ✅        | ✅     |
| Configuracion    | ✅    | ❌        | ❌     |
| Usuarios         | ✅    | ❌        | ❌     |
| Donantes         | ✅    | ✅        | ❌     |
| Donaciones       | ✅    | ✅        | ❌     |
| Inventario       | ✅    | ✅        | ❌     |
| Solicitudes      | ✅    | ✅        | ✅     |
| Transfusiones    | ✅    | ✅        | ✅     |

> El admin predefinido puede crear usuarios adicionales con rol admin desde la vista Usuarios.
> El endpoint de registro solo permite crear usuarios con rol medico o enfermero mediante matricula.
