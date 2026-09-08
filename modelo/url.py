"""
Clase URL: representa una dirección a analizar.
Aquí se aplica el pilar de ENCAPSULACION mediante atributos
privados y propiedades de solo lectura (@property).
"""
from urllib.parse import urlparse


class URL:
    def __init__(self, direccion):
        # Atributo privado: no se accede directamente desde fuera.
        self.__direccion = direccion.strip()
        # Se descompone la URL una sola vez y se guarda.
        self.__partes = urlparse(self.__direccion)

    # ---- ENCAPSULACION: propiedades de solo lectura ----
    @property
    def direccion(self):
        """Devuelve la direccion completa de la URL."""
        return self.__direccion

    @property
    def dominio(self):
        """Devuelve solo el dominio (netloc) de la URL."""
        return self.__partes.netloc

    @property
    def longitud(self):
        """Devuelve la cantidad de caracteres de la URL."""
        return len(self.__direccion)

    @property
    def protocolo(self):
        """Devuelve el esquema: http, https, etc."""
        return self.__partes.scheme

    # ---- Metodos de apoyo que usaran las reglas ----
    def contar_subdominios(self):
        """Cuenta los puntos del dominio como aproximacion a subdominios."""
        if not self.dominio:
            return 0
        return self.dominio.count(".")

    def __str__(self):
        return self.__direccion