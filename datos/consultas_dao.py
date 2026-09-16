"""
Consultas de negocio para el Detector de Phishing.
Contiene 5 consultas: 3 con JOIN y 3 con funciones de agregacion.
Todas viven aqui: la vista solo llama estos metodos.
"""
from datos.conexion import obtener_conexion


class ConsultasDAO:

    # 1) JOIN de 3 tablas: cada analisis con su URL y su nivel de riesgo
    def analisis_detallado(self):
        sql = """
            SELECT a.id_analisis, u.direccion, n.nombre AS nivel,
                   a.puntaje_total, a.veredicto_externo, a.fecha
            FROM ANALISIS a
            INNER JOIN URL u          ON a.id_url   = u.id_url
            INNER JOIN NIVEL_RIESGO n ON a.id_nivel = n.id_nivel
            ORDER BY a.fecha DESC;
        """
        return self._ejecutar(sql)

    # 2) JOIN + agregacion: reglas mas activadas (alimenta la Grafica 1)
    def reglas_mas_activadas(self):
        sql = """
            SELECT r.nombre, COUNT(*) AS veces_activada
            FROM ANALISIS_REGLA ar
            INNER JOIN REGLA r ON ar.id_regla = r.id_regla
            WHERE ar.activada = 1
            GROUP BY r.nombre
            ORDER BY veces_activada DESC;
        """
        return self._ejecutar(sql)

    # 3) JOIN + agregacion: cantidad de analisis por nivel (alimenta la Grafica 2)
    def analisis_por_nivel(self):
        sql = """
            SELECT n.nombre, COUNT(a.id_analisis) AS total
            FROM NIVEL_RIESGO n
            LEFT JOIN ANALISIS a ON a.id_nivel = n.id_nivel
            GROUP BY n.nombre
            ORDER BY total DESC;
        """
        return self._ejecutar(sql)

    # 4) Agregacion: promedio de puntaje por nivel de riesgo
    def promedio_puntaje_por_nivel(self):
        sql = """
            SELECT n.nombre, AVG(CAST(a.puntaje_total AS FLOAT)) AS promedio
            FROM NIVEL_RIESGO n
            INNER JOIN ANALISIS a ON a.id_nivel = n.id_nivel
            GROUP BY n.nombre
            ORDER BY promedio DESC;
        """
        return self._ejecutar(sql)

    # 5) JOIN + consulta parametrizada: URLs con puntaje mayor o igual a un umbral
    def urls_peligrosas(self, umbral):
        sql = """
            SELECT u.direccion, a.puntaje_total, a.veredicto_externo
            FROM ANALISIS a
            INNER JOIN URL u ON a.id_url = u.id_url
            WHERE a.puntaje_total >= ?
            ORDER BY a.puntaje_total DESC;
        """
        return self._ejecutar(sql, (umbral,))

    # --- helper interno ---
    def _ejecutar(self, sql, parametros=None):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        finally:
            conexion.close()
