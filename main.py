"""
main.py - Punto de entrada de la aplicacion.
Detector heuristico de phishing en URLs.
Arranca la interfaz grafica (Tkinter). La logica del modelo
y el controlador son los mismos del Entregable 2 (arquitectura MVC).
"""
from vista.vista_grafica import VistaGrafica


def main():
    app = VistaGrafica()
    app.iniciar()


if __name__ == "__main__":
    main()