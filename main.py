"""
main.py - Punto de entrada de la aplicacion.
Detector heuristico de phishing en URLs.
Arranca la vista de consola, que a su vez coordina
el controlador y el modelo (arquitectura MVC).
"""
from vista.vista_consola import VistaConsola


def main():
    app = VistaConsola()
    app.iniciar()


if __name__ == "__main__":
    main()
    