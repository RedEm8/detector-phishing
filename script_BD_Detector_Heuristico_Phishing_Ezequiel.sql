/* ============================================================
   DETECTOR HEURISTICO DE PHISHING EN URLs
   Entregable 4  -  Script de base de datos
   Motor: Microsoft SQL Server
   Autor: Ezequiel Musseb
   ============================================================ */

/* ---- 1. Crear la base de datos si no existe ---- */
IF DB_ID('DetectorPhishingDB') IS NULL
    CREATE DATABASE DetectorPhishingDB;
GO

USE DetectorPhishingDB;
GO

/* ---- 2. Eliminar tablas previas (orden inverso a las FK)
        Permite volver a ejecutar el script sin errores ---- */
DROP TABLE IF EXISTS ANALISIS_REGLA;
DROP TABLE IF EXISTS ANALISIS;
DROP TABLE IF EXISTS REGLA;
DROP TABLE IF EXISTS NIVEL_RIESGO;
DROP TABLE IF EXISTS URL;
GO

/* ============================================================
   3. CREACION DEL ESQUEMA (DDL)
   ============================================================ */

/* Tabla catalogo: niveles de riesgo */
CREATE TABLE NIVEL_RIESGO (
    id_nivel     INT IDENTITY(1,1) PRIMARY KEY,
    nombre       VARCHAR(20)  NOT NULL,
    descripcion  VARCHAR(100)
);
GO

/* URLs analizadas */
CREATE TABLE URL (
    id_url         INT IDENTITY(1,1) PRIMARY KEY,
    direccion      VARCHAR(255) NOT NULL,
    dominio        VARCHAR(100),
    longitud       INT,
    fecha_registro DATETIME NOT NULL DEFAULT GETDATE()
);
GO

/* Reglas heuristicas */
CREATE TABLE REGLA (
    id_regla     INT IDENTITY(1,1) PRIMARY KEY,
    nombre       VARCHAR(50)  NOT NULL,
    peso         INT          NOT NULL,
    descripcion  VARCHAR(150)
);
GO

/* Analisis realizados (cada analisis pertenece a una URL y a un nivel) */
CREATE TABLE ANALISIS (
    id_analisis       INT IDENTITY(1,1) PRIMARY KEY,
    id_url            INT NOT NULL,
    id_nivel          INT NOT NULL,
    puntaje_total     INT NOT NULL,
    veredicto_externo VARCHAR(50),
    fecha             DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_analisis_url   FOREIGN KEY (id_url)   REFERENCES URL(id_url),
    CONSTRAINT FK_analisis_nivel FOREIGN KEY (id_nivel) REFERENCES NIVEL_RIESGO(id_nivel)
);
GO

/* Tabla puente M:N -> que reglas se dispararon en cada analisis */
CREATE TABLE ANALISIS_REGLA (
    id_analisis INT NOT NULL,
    id_regla    INT NOT NULL,
    activada    BIT NOT NULL,
    CONSTRAINT PK_analisis_regla PRIMARY KEY (id_analisis, id_regla),
    CONSTRAINT FK_ar_analisis FOREIGN KEY (id_analisis) REFERENCES ANALISIS(id_analisis),
    CONSTRAINT FK_ar_regla    FOREIGN KEY (id_regla)    REFERENCES REGLA(id_regla)
);
GO

/* ============================================================
   4. DATOS DE PRUEBA (DML)  -  34 registros distribuidos
   ============================================================ */

/* --- Niveles de riesgo (4) --- */
INSERT INTO NIVEL_RIESGO (nombre, descripcion) VALUES
('Bajo',    'Sin indicios significativos de phishing'),
('Medio',   'Algunos indicios; se recomienda precaucion'),
('Alto',    'Multiples indicios de phishing'),
('Critico', 'Phishing casi seguro; no acceder');
GO

/* --- Reglas heuristicas (5) --- */
INSERT INTO REGLA (nombre, peso, descripcion) VALUES
('IP en URL',            25, 'Uso de una direccion IP en lugar de un nombre de dominio'),
('Simbolo arroba',       20, 'Presencia del caracter @ en la URL'),
('URL larga',            15, 'Longitud de la URL mayor a 75 caracteres'),
('Guiones excesivos',    10, 'Uso de multiples guiones en el dominio'),
('Palabras sospechosas', 30, 'Palabras como login, verify, secure o banco en la URL');
GO

/* --- URLs (6) --- */
INSERT INTO URL (direccion, dominio, longitud) VALUES
('https://www.google.com', 'google.com', 22),
('http://192.168.10.5/login/verify.php', '192.168.10.5', 36),
('https://secure-banco-actualizar.com/login', 'secure-banco-actualizar.com', 41),
('https://www.paypal.com', 'paypal.com', 22),
('http://verify-account@paypa1.com/update', 'paypa1.com', 39),
('https://mi-banco-seguro-verificacion-cuenta.com/acceso-urgente', 'mi-banco-seguro-verificacion-cuenta.com', 62);
GO

/* --- Analisis (6) --- */
INSERT INTO ANALISIS (id_url, id_nivel, puntaje_total, veredicto_externo) VALUES
(1, 1,  0, 'Limpio (VirusTotal)'),
(2, 3, 55, 'Sospechoso'),
(3, 2, 40, 'Sospechoso'),
(4, 1,  0, 'Limpio (VirusTotal)'),
(5, 4, 50, 'Malicioso (VirusTotal)'),
(6, 3, 55, 'No disponible');
GO

/* --- Analisis-Regla: reglas disparadas por analisis (13) --- */
INSERT INTO ANALISIS_REGLA (id_analisis, id_regla, activada) VALUES
(1, 3, 0),
(1, 5, 0),
(2, 1, 1),
(2, 5, 1),
(2, 3, 0),
(3, 4, 1),
(3, 5, 1),
(4, 5, 0),
(5, 2, 1),
(5, 5, 1),
(6, 3, 1),
(6, 4, 1),
(6, 5, 1);
GO

/* ============================================================
   5. Verificacion rapida (conteo por tabla)
   ============================================================ */
SELECT 'NIVEL_RIESGO'   AS tabla, COUNT(*) AS registros FROM NIVEL_RIESGO
UNION ALL SELECT 'REGLA',          COUNT(*) FROM REGLA
UNION ALL SELECT 'URL',            COUNT(*) FROM URL
UNION ALL SELECT 'ANALISIS',       COUNT(*) FROM ANALISIS
UNION ALL SELECT 'ANALISIS_REGLA', COUNT(*) FROM ANALISIS_REGLA;
GO