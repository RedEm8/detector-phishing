"""
Modulo de conexion a la base de datos SQL Server.
Centraliza la cadena de conexion y el manejo de errores.
Ninguna otra parte del programa crea conexiones por su cuenta.
"""
import pyodbc


# --- Excepcion personalizada para errores de base de datos ---
class ErrorConexionBD(Exception):
    """Se lanza cuando no se puede conectar a la base de datos."""
    pass


# --- Parametros de conexion (ajusta SERVIDOR a tu instancia) ---
SERVIDOR = r"LAPTOP-NC66HTOS\SQLEXPRESS"
BASE_DATOS = "DetectorPhishingDB"
DRIVER = "{ODBC Driver 17 for SQL Server}"

CADENA_CONEXION = (
    f"DRIVER={DRIVER};"
    f"SERVER={SERVIDOR};"
    f"DATABASE={BASE_DATOS};"
    f"Trusted_Connection=yes;"
)


def obtener_conexion():
    """
    Crea y devuelve una conexion a SQL Server.
    Lanza ErrorConexionBD con un mensaje claro si algo falla,
    sin exponer la traza tecnica al usuario.
    """
    try:
        conexion = pyodbc.connect(CADENA_CONEXION)
        return conexion
    except pyodbc.Error as e:
        raise ErrorConexionBD(
            "No se pudo conectar a la base de datos. Verifique que "
            "SQL Server este encendido y que el nombre del servidor "
            "sea correcto."
        ) from e