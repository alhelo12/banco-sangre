# Base de Datos — Banco de Sangre

Motor: **PostgreSQL 16**

---

## Diagrama de Relaciones

```
usuarios
   (sin relaciones directas con otras tablas)

configuracion_roles
   (sin relaciones directas, define prefijos de matricula para el registro)

donantes
   │
   └──< donaciones (1 donante puede tener muchas donaciones)
              │
              └──< inventario_sangre (1 donacion genera 1 unidad en inventario)
                          │
                          └──< transfusiones (1 unidad puede usarse en 1 transfusion)

solicitudes
   │
   └──< transfusiones (1 solicitud genera 1 transfusion)
```

---

## Tablas y Relaciones

### 1. `usuarios`
Almacena los usuarios del sistema. No tiene relaciones con otras tablas.

| Campo      | Tipo         | Descripcion                          |
|------------|--------------|--------------------------------------|
| id         | SERIAL PK    | Identificador unico                  |
| nombre     | VARCHAR(100) | Nombre del usuario                   |
| email      | VARCHAR(100) | Email unico, usado para login        |
| password   | VARCHAR(255) | Contrasena hasheada con bcrypt       |
| rol        | ENUM         | admin / enfermero / medico           |
| created_at | TIMESTAMP    | Fecha de creacion                    |

**Usuario admin por defecto:**
- Email: `admin@bancosangre.com`
- Password: `admin123`

---

### 2. `donantes`
Almacena los datos personales de cada donante.

| Campo      | Tipo         | Descripcion                          |
|------------|--------------|--------------------------------------|
| id         | SERIAL PK    | Identificador unico                  |
| nombre     | VARCHAR(100) | Nombre del donante                   |
| apellido   | VARCHAR(100) | Apellido del donante                 |
| fecha_nac  | DATE         | Fecha de nacimiento                  |
| tipo_sangre| VARCHAR(5)   | Tipo de sangre: A+, O-, AB+, etc.    |
| telefono   | VARCHAR(20)  | Telefono de contacto (opcional)      |
| email      | VARCHAR(100) | Email de contacto (opcional)         |
| created_at | TIMESTAMP    | Fecha de registro                    |

**Relaciones:**
- Un `donante` puede tener **muchas** `donaciones` → `donaciones.donante_id`

---

### 3. `donaciones`
Registro de cada donacion realizada por un donante.

| Campo      | Tipo         | Descripcion                          |
|------------|--------------|--------------------------------------|
| id         | SERIAL PK    | Identificador unico                  |
| donante_id | INT FK       | Referencia a `donantes.id`           |
| fecha      | TIMESTAMP    | Fecha y hora de la donacion          |
| volumen_ml | DECIMAL(6,2) | Volumen donado en ml (default 450)   |
| estado     | ENUM         | pendiente / aprobada / rechazada     |
| notas      | VARCHAR(300) | Observaciones adicionales (opcional) |

**Relaciones:**
- Pertenece a un `donante` → `donante_id`
- Una `donacion` aprobada genera **una** unidad en `inventario_sangre`

---

### 4. `inventario_sangre`
Stock de unidades de sangre disponibles para transfusion.

| Campo       | Tipo         | Descripcion                          |
|-------------|--------------|--------------------------------------|
| id          | SERIAL PK    | Identificador unico                  |
| donacion_id | INT FK       | Referencia a `donaciones.id`         |
| tipo_sangre | VARCHAR(5)   | Tipo de sangre de la unidad          |
| componente  | VARCHAR(50)  | sangre total / plasma / plaquetas    |
| volumen_ml  | DECIMAL(6,2) | Volumen disponible en ml             |
| fecha_exp   | DATE         | Fecha de vencimiento                 |
| disponible  | BOOLEAN      | TRUE = disponible, FALSE = usado     |

**Relaciones:**
- Proviene de una `donacion` → `donacion_id`
- Una unidad puede ser usada en **una** `transfusion`

---

### 5. `solicitudes`
Pedidos de sangre para pacientes.

| Campo       | Tipo         | Descripcion                              |
|-------------|--------------|------------------------------------------|
| id          | SERIAL PK    | Identificador unico                      |
| paciente    | VARCHAR(150) | Nombre del paciente                      |
| tipo_sangre | VARCHAR(5)   | Tipo de sangre requerido                 |
| volumen_ml  | DECIMAL(6,2) | Volumen solicitado en ml                 |
| medico      | VARCHAR(150) | Medico solicitante (opcional)            |
| hospital    | VARCHAR(150) | Hospital de destino (opcional)           |
| estado      | ENUM         | pendiente / aprobada / rechazada / entregada |
| fecha       | TIMESTAMP    | Fecha y hora de la solicitud             |
| notas       | VARCHAR(300) | Observaciones adicionales (opcional)     |

**Relaciones:**
- Una `solicitud` aprobada genera **una** `transfusion`

---

### 6. `transfusiones`
Registro de entregas de sangre a pacientes.

| Campo          | Tipo         | Descripcion                          |
|----------------|--------------|--------------------------------------|
| id             | SERIAL PK    | Identificador unico                  |
| solicitud_id   | INT FK       | Referencia a `solicitudes.id`        |
| inventario_id  | INT FK       | Referencia a `inventario_sangre.id`  |
| fecha          | TIMESTAMP    | Fecha y hora de la transfusion       |
| realizada_por  | VARCHAR(150) | Nombre del profesional (opcional)    |
| observaciones  | VARCHAR(300) | Observaciones adicionales (opcional) |

**Relaciones:**
- Pertenece a una `solicitud` → `solicitud_id`
- Consume una unidad de `inventario_sangre` → `inventario_id`

---

### 7. `configuracion_roles`
Define los prefijos de matricula que identifican cada rol al momento del registro.

| Campo       | Tipo         | Descripcion                              |
|-------------|--------------|------------------------------------------|
| id          | SERIAL PK    | Identificador unico                      |
| prefijo     | VARCHAR(20)  | Prefijo de la matricula (Ej: MED, ENF)   |
| rol         | ENUM         | medico / enfermero                       |
| descripcion | VARCHAR(100) | Descripcion del grupo (opcional)         |

**Registros iniciales:**
- `MED` → medico
- `ENF` → enfermero

> El admin puede agregar, editar o eliminar prefijos desde la app en la seccion Configuracion.

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

---

## Flujo principal

```
1. El admin configura los prefijos de matricula en Configuracion
2. El personal se registra con su matricula del hospital
   → el sistema asigna el rol automaticamente segun el prefijo
3. Se registra un DONANTE
4. El donante realiza una DONACION  →  estado: pendiente
5. La donacion es revisada          →  estado: aprobada / rechazada
6. Si es aprobada, se agrega al     →  INVENTARIO_SANGRE (disponible: true)
7. Se recibe una SOLICITUD          →  estado: pendiente
8. La solicitud es aprobada         →  estado: aprobada
9. Se asigna una unidad del         →  INVENTARIO a la solicitud
10. Se registra la TRANSFUSION      →  inventario disponible: false
                                        solicitud estado: entregada
```
