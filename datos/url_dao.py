"""
DAO (Data Access Object) para la entidad URL.
Toda la logica SQL de la tabla URL vive aqui.
La vista NUNCA escribe SQL: solo llama a estos metodos.
"""
from datos.conexion import obtener_conexion


class UrlDAO:

    def crear(self, direccion, dominio, longitud):
        """CREATE: inserta una nueva URL."""
        sql = "INSERT INTO URL (direccion, dominio, longitud) VALUES (?, ?, ?);"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (direccion, dominio, longitud))
            conexion.commit()
        finally:
            conexion.close()

    def listar(self):
        """READ: devuelve todas las URLs."""
        sql = ("SELECT id_url, direccion, dominio, longitud "
               "FROM URL ORDER BY id_url;")
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            conexion.close()

    def obtener_por_id(self, id_url):
        """READ: devuelve una URL por su id, o None si no existe."""
        sql = ("SELECT id_url, direccion, dominio, longitud "
               "FROM URL WHERE id_url = ?;")
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_url,))
            return cursor.fetchone()
        finally:
            conexion.close()

    def actualizar(self, id_url, direccion, dominio, longitud):
        """UPDATE: modifica una URL existente."""
        sql = ("UPDATE URL SET direccion = ?, dominio = ?, longitud = ? "
               "WHERE id_url = ?;")
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (direccion, dominio, longitud, id_url))
            conexion.commit()
        finally:
            conexion.close()

    def eliminar(self, id_url):
        """DELETE: elimina una URL por su id."""
        sql = "DELETE FROM URL WHERE id_url = ?;"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_url,))
            conexion.commit()
        finally:
            conexion.close()
