"""
Cliente de la API de VirusTotal (v3) para verificar URLs.
Usa SOLO la biblioteca estandar de Python (urllib), sin pip install.
Aporta un veredicto externo que refuerza el analisis heuristico local
(defensa en profundidad: una segunda opinion independiente).
"""
import os
import json
import base64
import urllib.request
import urllib.error


class ErrorVirusTotal(Exception):
    """Error al consultar la API de VirusTotal."""
    pass


# La clave NUNCA se escribe en el codigo: se lee de una variable de entorno.
API_KEY = os.environ.get("VT_API_KEY", "")
BASE_URL = "https://www.virustotal.com/api/v3/urls/"
TIMEOUT = 15  # segundos


def _id_de_url(url):
    """VirusTotal identifica una URL por su base64 url-safe sin relleno '='."""
    return base64.urlsafe_b64encode(url.encode()).decode().strip("=")


def verificar_url(url):
    """
    Consulta el reporte de una URL en VirusTotal.
    Devuelve un dict: {veredicto, maliciosos, sospechosos, total}.
    Lanza ErrorVirusTotal si algo falla (clave, red, limite, etc.).
    """
    if not API_KEY:
        raise ErrorVirusTotal("Falta la clave de API (variable de entorno VT_API_KEY).")

    endpoint = BASE_URL + _id_de_url(url)
    peticion = urllib.request.Request(endpoint, headers={"x-apikey": API_KEY})

    try:
        with urllib.request.urlopen(peticion, timeout=TIMEOUT) as respuesta:
            datos = json.loads(respuesta.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # La URL todavia no ha sido analizada por VirusTotal.
            return {"veredicto": "No analizada", "maliciosos": 0,
                    "sospechosos": 0, "total": 0}
        if e.code == 401:
            raise ErrorVirusTotal("Clave de API invalida.") from e
        if e.code == 429:
            raise ErrorVirusTotal("Limite de consultas alcanzado. Intente en un minuto.") from e
        raise ErrorVirusTotal(f"VirusTotal devolvio un error (codigo {e.code}).") from e
    except urllib.error.URLError as e:
        raise ErrorVirusTotal("No hay conexion a internet o el servicio no responde.") from e

    # Estadisticas del ultimo analisis: cuantos motores marcaron la URL.
    stats = datos["data"]["attributes"]["last_analysis_stats"]
    maliciosos = stats.get("malicious", 0)
    sospechosos = stats.get("suspicious", 0)
    total = sum(stats.values())

    if maliciosos > 0:
        veredicto = "Malicioso"
    elif sospechosos > 0:
        veredicto = "Sospechoso"
    else:
        veredicto = "Limpio"

    return {"veredicto": veredicto, "maliciosos": maliciosos,
            "sospechosos": sospechosos, "total": total}


# Prueba rapida:  python -m datos.virustotal_api   (con VT_API_KEY configurada)
if __name__ == "__main__":
    try:
        print(verificar_url("https://www.google.com"))
    except ErrorVirusTotal as e:
        print("Error:", e)