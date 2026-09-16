# Detector Heurístico de Phishing en URLs

Aplicación de escritorio que analiza URLs y estima la probabilidad de que sean
phishing, aplicando reglas heurísticas ponderadas y una verificación externa.
Los resultados se almacenan en una base de datos SQL Server y se visualizan
mediante gráficas.

Proyecto del módulo **Técnico en Ciberseguridad – INFOTEP**.
Arquitectura **MVC** con capa de acceso a datos (patrón **DAO**).

---

## Requisitos

- **Python 3.10 o superior**
- **Microsoft SQL Server** (Express o superior) en ejecución
- **ODBC Driver 17 for SQL Server** instalado
- Librería **pyodbc** (`pip install pyodbc`)
- Librería **matplotlib** (`pip install matplotlib`)

> El resto del proyecto usa solo la biblioteca estándar de Python
> (`tkinter`, `json`, etc.).

---

## Instalación

1. Clonar o descomprimir el proyecto:

   ```
   git clone https://github.com/RedEm8/detector-phishing.git
   cd detector-phishing
   ```

2. Instalar las dependencias:

   ```
   pip install pyodbc matplotlib
   ```

---

## Crear la base de datos

1. Abrir **SQL Server Management Studio (SSMS)** y conectarse a la instancia local.
2. Abrir el archivo **`DetectorPhishingDB.sql`** incluido en el proyecto.
3. Ejecutarlo (**F5**). Esto crea la base de datos `DetectorPhishingDB`,
   las 5 tablas y carga los datos de prueba.
4. Verificar que aparezca el conteo por tabla al final (4, 5, 6, 6, 13).

Alternativa por consola:

```
sqlcmd -S NOMBRE_SERVIDOR\SQLEXPRESS -i DetectorPhishingDB.sql
```

---

## Configurar la conexión

Editar el archivo **`datos/conexion.py`** y ajustar el nombre del servidor a
su instancia local:

```python
SERVIDOR = r"NOMBRE_SERVIDOR\SQLEXPRESS"
```

Para ver el nombre de su instancia, use en SSMS: `SELECT @@SERVERNAME;`.

---

## Ejecutar la aplicación

Desde la carpeta raíz del proyecto:

```
python main.py
```

Para probar solo el módulo de gestión de datos y gráficas del Entregable 4:

```
python -m vista.vista_bd
```

---

## Estructura del proyecto

```
detector_phishing/
├── modelo/            # Clases del dominio (URL, Resultado, Regla, etc.)
├── vista/             # Interfaz gráfica (Tkinter)
│   └── vista_bd.py    # Pestañas CRUD + gráficas desde la BD
├── controlador/       # Lógica de coordinación
├── datos/             # Capa de acceso a datos (DAO)
│   ├── conexion.py    # Conexión centralizada a SQL Server
│   ├── regla_dao.py   # CRUD de la entidad REGLA
│   ├── url_dao.py     # CRUD de la entidad URL
│   └── consultas_dao.py  # Consultas de negocio (JOIN y agregación)
├── DetectorPhishingDB.sql  # Script de creación de la base de datos
├── main.py            # Punto de entrada
└── README.md
```

---

## Autor

**Ezequiel Musseb** — Técnico en Ciberseguridad, INFOTEP.
Repositorio: https://github.com/RedEm8/detector-phishing
