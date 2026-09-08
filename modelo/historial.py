"""
Clase Historial: gestiona la lista de resultados y su PERSISTENCIA.
Guarda y carga los analisis en un archivo JSON, de modo que los
datos sobreviven al cierre del programa. Usa try/except para
proteger las operaciones de lectura/escritura de archivos.
"""
import json
import os


class Historial:
    def __init__(self, ruta_archivo="datos/historial.json"):
        self._ruta = ruta_archivo
        self._resultados = []
        self.cargar()  # al crear el historial, intenta cargar lo guardado

    def agregar(self, resultado):
        """Agrega un resultado nuevo y lo persiste de inmediato."""
        self._resultados.append(resultado.to_dict())
        self.guardar()

    def obtener_todos(self):
        """Devuelve la lista de todos los analisis guardados."""
        return list(self._resultados)

    def guardar(self):
        """Escribe la lista de resultados al archivo JSON."""
        try:
            # Se asegura de que la carpeta 'datos' exista.
            carpeta = os.path.dirname(self._ruta)
            if carpeta and not os.path.exists(carpeta):
                os.makedirs(carpeta)

            with open(self._ruta, "w", encoding="utf-8") as f:
                json.dump(self._resultados, f, indent=4, ensure_ascii=False)
        except (IOError, OSError) as e:
            print(f"Error al guardar el historial: {e}")

    def cargar(self):
        """Lee los resultados desde el archivo JSON si existe."""
        try:
            if os.path.exists(self._ruta):
                with open(self._ruta, "r", encoding="utf-8") as f:
                    self._resultados = json.load(f)
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error al cargar el historial: {e}")
            self._resultados = []