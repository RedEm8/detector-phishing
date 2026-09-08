"""
Clase Resultado: representa el veredicto de un analisis de URL.
Aplica ENCAPSULACION con atributos privados, propiedades de solo
lectura y una propiedad con validacion (setter) para el nivel de riesgo.
"""
from datetime import datetime


class Resultado:
    # Niveles de riesgo validos que acepta la clase.
    NIVELES_VALIDOS = ("segura", "sospechosa", "peligrosa")

    def __init__(self, url, puntaje_total):
        self.__url = url                      # texto de la URL analizada
        self.__puntaje_total = puntaje_total  # suma de pesos de las reglas
        self.__senales = []                   # lista de reglas que se activaron
        self.__nivel_riesgo = "segura"        # valor inicial por defecto
        self.__fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ---- ENCAPSULACION: propiedades de solo lectura ----
    @property
    def url(self):
        return self.__url

    @property
    def puntaje_total(self):
        return self.__puntaje_total

    @property
    def senales(self):
        # Se devuelve una copia para que nadie modifique la lista original.
        return list(self.__senales)

    @property
    def fecha(self):
        return self.__fecha

    # ---- ENCAPSULACION: propiedad CON validacion (getter + setter) ----
    @property
    def nivel_riesgo(self):
        return self.__nivel_riesgo

    @nivel_riesgo.setter
    def nivel_riesgo(self, valor):
        if valor not in self.NIVELES_VALIDOS:
            raise ValueError(
                f"Nivel invalido: '{valor}'. "
                f"Debe ser uno de {self.NIVELES_VALIDOS}"
            )
        self.__nivel_riesgo = valor

    # ---- Metodos de apoyo ----
    def agregar_senal(self, descripcion):
        """Registra una senal (motivo) detectada durante el analisis."""
        self.__senales.append(descripcion)

    def to_dict(self):
        """Convierte el resultado a diccionario (util para guardar en JSON)."""
        return {
            "url": self.__url,
            "puntaje_total": self.__puntaje_total,
            "nivel_riesgo": self.__nivel_riesgo,
            "senales": self.__senales,
            "fecha": self.__fecha,
        }

    def __str__(self):
        return f"[{self.__nivel_riesgo.upper()}] {self.__url} ({self.__puntaje_total} pts)"