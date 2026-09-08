"""
Clase abstracta Regla: es el molde base de todas las reglas heuristicas.
Aplica el pilar de ABSTRACCION usando ABC y @abstractmethod.
Ninguna regla se usa directamente: cada regla hija hereda de aqui
y define su propia version del metodo evaluar().
"""
from abc import ABC, abstractmethod


class Regla(ABC):
    def __init__(self, nombre, peso):
        # Atributos protegidos (un guion bajo): las hijas pueden usarlos.
        self._nombre = nombre
        self._peso = peso

    @property
    def nombre(self):
        return self._nombre

    @property
    def peso(self):
        return self._peso

    # ---- ABSTRACCION: metodo obligatorio que las hijas DEBEN implementar ----
    @abstractmethod
    def evaluar(self, url):
        """
        Evalua una URL y devuelve el puntaje de riesgo de esta regla.
        Cada regla hija define su propia logica aqui.
        """
        pass

    def __str__(self):
        return f"Regla: {self._nombre} (peso {self._peso})"