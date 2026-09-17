"""
DAO (Data Access Object) para la entidad REGLA.
Toda la logica SQL de la tabla REGLA vive aqui.
La vista NUNCA escribe SQL: solo llama a estos metodos.
"""
from datos.conexion import obtener_conexion


class ReglaDAO:

    def crear(self, nombre, peso, descripcion):
        """CREATE: inserta una nueva regla."""
        sql = "INSERT INTO REGLA (nombre, peso, descripcion) VALUES (?, ?, ?);"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (nombre, peso, descripcion))
            conexion.commit()
        finally:
            conexion.close()

    def listar(self):
        """READ: devuelve todas las reglas."""
        sql = "SELECT id_regla, nombre, peso, descripcion FROM REGLA ORDER BY id_regla;"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            conexion.close()

    def obtener_por_id(self, id_regla):
        """READ: devuelve una regla por su id, o None si no existe."""
        sql = "SELECT id_regla, nombre, peso, descripcion FROM REGLA WHERE id_regla = ?;"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_regla,))
            return cursor.fetchone()
        finally:
            conexion.close()

    def actualizar(self, id_regla, nombre, peso, descripcion):
        """UPDATE: modifica una regla existente."""
        sql = "UPDATE REGLA SET nombre = ?, peso = ?, descripcion = ? WHERE id_regla = ?;"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (nombre, peso, descripcion, id_regla))
            conexion.commit()
        finally:
            conexion.close()

    def eliminar(self, id_regla):
        """DELETE: elimina una regla por su id."""
        sql = "DELETE FROM REGLA WHERE id_regla = ?;"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_regla,))
            conexion.commit()
        finally:
            conexion.close()