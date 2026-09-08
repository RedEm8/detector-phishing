"""
Clase MotorHeuristico: coordina todas las reglas heuristicas.
Recorre las reglas y llama a evaluar(url) en cada una de forma
UNIFORME (POLIMORFISMO), suma los puntajes, arma el Resultado
y clasifica el nivel de riesgo segun los umbrales definidos.
"""
from modelo.resultado import Resultado


class MotorHeuristico:
    # Umbrales de clasificacion (puntaje maximo posible: 95)
    UMBRAL_SOSPECHOSA = 30
    UMBRAL_PELIGROSA = 60

    def __init__(self):
        # El motor esta COMPUESTO por una lista de reglas.
        self._reglas = []

    def agregar_regla(self, regla):
        """Agrega una regla al motor."""
        self._reglas.append(regla)

    def analizar(self, url):
        """
        Aplica todas las reglas a la URL y devuelve un Resultado.
        Aqui ocurre el POLIMORFISMO: se llama a regla.evaluar(url)
        sin importar de que tipo de regla se trate.
        """
        puntaje_total = 0
        senales = []

        for regla in self._reglas:
            puntaje = regla.evaluar(url)   # <-- llamada polimorfica uniforme
            if puntaje > 0:
                puntaje_total += puntaje
                senales.append(f"{regla.nombre} (+{puntaje})")

        # Se construye el resultado
        resultado = Resultado(str(url), puntaje_total)
        resultado.nivel_riesgo = self._clasificar(puntaje_total)
        for senal in senales:
            resultado.agregar_senal(senal)

        return resultado

    def _clasificar(self, puntaje):
        """Traduce un puntaje numerico a un nivel de riesgo."""
        if puntaje >= self.UMBRAL_PELIGROSA:
            return "peligrosa"
        elif puntaje >= self.UMBRAL_SOSPECHOSA:
            return "sospechosa"
        else:
            return "segura"