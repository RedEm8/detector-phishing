"""
Clase URL: representa una direccion a analizar.
Aplica ENCAPSULACION con atributos privados y propiedades.
Valida la direccion al construirse y lanza URLInvalidaError
si el formato no es correcto (MANEJO DE EXCEPCIONES).
"""
from urllib.parse import urlparse
from modelo.excepciones import URLInvalidaError


class URL:
    def __init__(self, direccion):
        # Validacion de entrada: operacion de riesgo protegida.
        if not direccion or not isinstance(direccion, str):
            raise URLInvalidaError("La URL esta vacia o no es texto")

        direccion = direccion.strip()

        if not direccion.startswith(("http://", "https://")):
            raise URLInvalidaError(
                "La URL debe comenzar con http:// o https://"
            )

        self.__direccion = direccion
        self.__partes = urlparse(self.__direccion)

        # Si tras el parseo no hay dominio, la URL es invalida.
        if not self.__partes.netloc:
            raise URLInvalidaError("La URL no contiene un dominio valido")

    @property
    def direccion(self):
        return self.__direccion

    @property
    def dominio(self):
        return self.__partes.netloc

    @property
    def longitud(self):
        return len(self.__direccion)

    @property
    def protocolo(self):
        return self.__partes.scheme

    def contar_subdominios(self):
        if not self.dominio:
            return 0
        return self.dominio.count(".")

    def __str__(self):
        return self.__direccion