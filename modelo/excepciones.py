"""
Excepciones personalizadas del proyecto.
Definir errores propios permite distinguir los problemas especificos
de la aplicacion de los errores genericos de Python.
"""


class URLInvalidaError(Exception):
    """Se lanza cuando una URL no tiene un formato valido para analizar."""
    def __init__(self, mensaje="La URL ingresada no es valida"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ReputacionNoDisponibleError(Exception):
    """Se lanza cuando la consulta de reputacion externa falla."""
    def __init__(self, mensaje="No se pudo consultar la reputacion externa"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)