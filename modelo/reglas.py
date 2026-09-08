"""
Reglas heuristicas concretas. Todas HEREDAN de la clase abstracta Regla
y aplican POLIMORFISMO: cada una implementa evaluar(url) a su manera,
pero el controlador las invoca de forma uniforme.
"""
from modelo.regla import Regla


class ReglaLongitud(Regla):
    """Penaliza URLs demasiado largas (tactica comun de ofuscacion)."""
    def __init__(self):
        super().__init__("Longitud excesiva", 15)
        self._limite = 54  # umbral tipico de URL sospechosa

    def evaluar(self, url):
        if url.longitud > self._limite:
            return self._peso
        return 0


class ReglaIP(Regla):
    """Detecta si se usa una direccion IP en lugar de un dominio."""
    def __init__(self):
        super().__init__("Uso de IP en lugar de dominio", 25)

    def evaluar(self, url):
        # Si el dominio empieza con un numero, probablemente es una IP.
        dominio = url.dominio
        if dominio and dominio.replace(".", "").split(":")[0].isdigit():
            return self._peso
        return 0


class ReglaPalabrasClave(Regla):
    """Detecta palabras sensibles usadas en phishing."""
    def __init__(self):
        super().__init__("Palabra clave sospechosa", 20)
        self._palabras = ["login", "verify", "secure", "account",
                          "update", "banco", "confirm", "signin"]

    def evaluar(self, url):
        direccion = url.direccion.lower()
        for palabra in self._palabras:
            if palabra in direccion:
                return self._peso
        return 0


class ReglaTyposquatting(Regla):
    """Detecta sustitucion de caracteres (ej: 0 por o, 1 por l)."""
    def __init__(self):
        super().__init__("Posible typosquatting", 20)
        self._sospechosos = ["0", "1", "3", "5", "@"]

    def evaluar(self, url):
        dominio = url.dominio.lower()
        # Marcas de banco/marcas conocidas con numeros mezclados.
        for caracter in self._sospechosos:
            if caracter in dominio:
                return self._peso
        return 0


class ReglaProtocolo(Regla):
    """Penaliza URLs que usan HTTP en lugar de HTTPS."""
    def __init__(self):
        super().__init__("Sin cifrado HTTPS", 15)

    def evaluar(self, url):
        if url.protocolo == "http":
            return self._peso
        return 0