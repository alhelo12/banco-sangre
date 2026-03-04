-- ============================================================
-- BANCO DE SANGRE - Schema de Base de Datos
-- Motor: PostgreSQL 16
-- ============================================================

-- Crear base de datos (ejecutar por separado si no existe)
-- CREATE DATABASE banco_sangre;

-- ============================================================
-- TIPOS ENUM
-- ============================================================

CREATE TYPE rol_usuario AS ENUM ('admin', 'enfermero', 'medico');
CREATE TYPE estado_donacion AS ENUM ('pendiente', 'aprobada', 'rechazada');
CREATE TYPE estado_solicitud AS ENUM ('pendiente', 'aprobada', 'rechazada', 'entregada');

-- ============================================================
-- TABLA 1: usuarios
-- Almacena los usuarios del sistema con su rol
-- ============================================================

CREATE TABLE usuarios (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    rol         rol_usuario  NOT NULL DEFAULT 'enfermero',
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABLA 2: donantes
-- Almacena los datos personales de cada donante
-- ============================================================

CREATE TABLE donantes (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    apellido    VARCHAR(100) NOT NULL,
    fecha_nac   DATE         NOT NULL,
    tipo_sangre VARCHAR(5)   NOT NULL,   -- Ej: A+, O-, AB+
    telefono    VARCHAR(20),
    email       VARCHAR(100),
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABLA 3: donaciones
-- Registro de cada donacion realizada por un donante
-- ============================================================

CREATE TABLE donaciones (
    id          SERIAL PRIMARY KEY,
    donante_id  INT              NOT NULL REFERENCES donantes(id) ON DELETE CASCADE,
    fecha       TIMESTAMP        NOT NULL DEFAULT NOW(),
    volumen_ml  DECIMAL(6,2)     NOT NULL DEFAULT 450.00,
    estado      estado_donacion  NOT NULL DEFAULT 'pendiente',
    notas       VARCHAR(300)
);

-- ============================================================
-- TABLA 4: inventario_sangre
-- Stock de unidades de sangre disponibles
-- ============================================================

CREATE TABLE inventario_sangre (
    id          SERIAL PRIMARY KEY,
    donacion_id INT          NOT NULL REFERENCES donaciones(id) ON DELETE CASCADE,
    tipo_sangre VARCHAR(5)   NOT NULL,
    componente  VARCHAR(50)  NOT NULL DEFAULT 'sangre total',  -- plasma, plaquetas, etc.
    volumen_ml  DECIMAL(6,2) NOT NULL,
    fecha_exp   DATE         NOT NULL,
    disponible  BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ============================================================
-- TABLA 5: solicitudes
-- Pedidos de sangre para pacientes
-- ============================================================

CREATE TABLE solicitudes (
    id          SERIAL PRIMARY KEY,
    paciente    VARCHAR(150)     NOT NULL,
    tipo_sangre VARCHAR(5)       NOT NULL,
    volumen_ml  DECIMAL(6,2)     NOT NULL,
    medico      VARCHAR(150),
    hospital    VARCHAR(150),
    estado      estado_solicitud NOT NULL DEFAULT 'pendiente',
    fecha       TIMESTAMP        NOT NULL DEFAULT NOW(),
    notas       VARCHAR(300)
);

-- ============================================================
-- TABLA 6: transfusiones
-- Registro de entregas de sangre a pacientes
-- ============================================================

CREATE TABLE transfusiones (
    id              SERIAL PRIMARY KEY,
    solicitud_id    INT          NOT NULL REFERENCES solicitudes(id) ON DELETE CASCADE,
    inventario_id   INT          NOT NULL REFERENCES inventario_sangre(id) ON DELETE CASCADE,
    fecha           TIMESTAMP    NOT NULL DEFAULT NOW(),
    realizada_por   VARCHAR(150),
    observaciones   VARCHAR(300)
);

-- ============================================================
-- TABLA 7: configuracion_roles
-- Define los prefijos de matricula que identifican cada rol
-- ============================================================

CREATE TABLE configuracion_roles (
    id         SERIAL PRIMARY KEY,
    prefijo    VARCHAR(20)  NOT NULL UNIQUE,  -- Ej: MED, ENF
    rol        rol_usuario  NOT NULL,          -- medico, enfermero
    descripcion VARCHAR(100)                   -- Ej: Medico general
);

-- Datos iniciales de ejemplo (el admin puede cambiarlos)
INSERT INTO configuracion_roles (prefijo, rol, descripcion) VALUES
('MED', 'medico',    'Personal medico'),
('ENF', 'enfermero', 'Personal de enfermeria');

-- ============================================================
-- INDICES (mejoran la velocidad de busqueda)
-- ============================================================

CREATE INDEX idx_donantes_tipo_sangre    ON donantes(tipo_sangre);
CREATE INDEX idx_donaciones_donante_id   ON donaciones(donante_id);
CREATE INDEX idx_donaciones_estado       ON donaciones(estado);
CREATE INDEX idx_inventario_tipo_sangre  ON inventario_sangre(tipo_sangre);
CREATE INDEX idx_inventario_disponible   ON inventario_sangre(disponible);
CREATE INDEX idx_solicitudes_estado      ON solicitudes(estado);
CREATE INDEX idx_solicitudes_tipo_sangre ON solicitudes(tipo_sangre);

-- ============================================================
-- DATOS INICIALES (usuario admin por defecto)
-- Email: admin@bancosangre.com (se usa para iniciar sesión)
-- password: admin123 (hasheada con bcrypt)
-- ============================================================

INSERT INTO usuarios (nombre, email, password, rol) VALUES
('Administrador', 'admin@bancosangre.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin');
