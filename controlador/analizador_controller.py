"""
Controlador principal: coordina el modelo con la vista.
Arma el motor con todas las reglas, gestiona el historial y
ofrece metodos limpios que la vista puede invocar. Aqui se
INVOCA el analisis polimorfico del motor sobre las reglas.
"""
from modelo.url import URL
from modelo.motor_heuristico import MotorHeuristico
from modelo.historial import Historial
from modelo.excepciones import URLInvalidaError
from modelo.reglas import (ReglaLongitud, ReglaIP, ReglaPalabrasClave,
                           ReglaTyposquatting, ReglaProtocolo)


class AnalizadorController:
    def __init__(self):
        # Se arma el motor con las cinco reglas heuristicas.
        self._motor = MotorHeuristico()
        self._motor.agregar_regla(ReglaLongitud())
        self._motor.agregar_regla(ReglaIP())
        self._motor.agregar_regla(ReglaPalabrasClave())
        self._motor.agregar_regla(ReglaTyposquatting())
        self._motor.agregar_regla(ReglaProtocolo())

        # Se carga el historial (con lo guardado en JSON).
        self._historial = Historial()

    def analizar_url(self, direccion):
        """
        Analiza una URL ingresada como texto.
        Devuelve el objeto Resultado. Lanza URLInvalidaError
        si la direccion no es valida (la vista lo maneja).
        """
        url = URL(direccion)               # puede lanzar URLInvalidaError
        resultado = self._motor.analizar(url)
        self._historial.agregar(resultado)  # se guarda automaticamente
        return resultado

    def obtener_historial(self):
        """Devuelve todos los analisis guardados."""
        return self._historial.obtener_todos()

    def obtener_estadisticas(self):
        """
        Devuelve estadisticas agregadas del historial para las graficas:
        - conteo por nivel de riesgo
        - conteo de veces que se activo cada regla
        """
        analisis = self._historial.obtener_todos()

        conteo_niveles = {"segura": 0, "sospechosa": 0, "peligrosa": 0}
        conteo_reglas = {}

        for a in analisis:
            nivel = a.get("nivel_riesgo", "segura")
            if nivel in conteo_niveles:
                conteo_niveles[nivel] += 1

            for senal in a.get("senales", []):
                nombre = senal.split(" (+")[0]
                conteo_reglas[nombre] = conteo_reglas.get(nombre, 0) + 1

        return {"niveles": conteo_niveles, "reglas": conteo_reglas}