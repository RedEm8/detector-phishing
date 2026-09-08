"""
Vista de consola: interfaz de texto que interactua con el usuario.
Es la unica capa que usa input() y print() y la que atrapa las
excepciones para mostrar mensajes claros. Toda la logica se delega
al controlador.
"""
from controlador.analizador_controller import AnalizadorController
from modelo.excepciones import URLInvalidaError


class VistaConsola:
    def __init__(self):
        self._ctrl = AnalizadorController()

    def mostrar_menu(self):
        print("\n" + "=" * 45)
        print("   DETECTOR HEURISTICO DE PHISHING")
        print("=" * 45)
        print("  1. Analizar una URL")
        print("  2. Ver historial de analisis")
        print("  3. Salir")
        print("=" * 45)

    def iniciar(self):
        """Bucle principal del programa."""
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opcion (1-3): ").strip()

            if opcion == "1":
                self._opcion_analizar()
            elif opcion == "2":
                self._opcion_historial()
            elif opcion == "3":
                print("\nSaliendo del programa. Hasta pronto!\n")
                break
            else:
                print("\n[!] Opcion no valida. Intente de nuevo.")

    def _opcion_analizar(self):
        """Pide una URL y muestra el veredicto con su desglose."""
        direccion = input("\nIngrese la URL a analizar: ").strip()
        try:
            resultado = self._ctrl.analizar_url(direccion)
            print("\n--- RESULTADO DEL ANALISIS ---")
            print(f"URL: {resultado.url}")
            print(f"Nivel de riesgo: {resultado.nivel_riesgo.upper()}")
            print(f"Puntaje total: {resultado.puntaje_total}")
            if resultado.senales:
                print("Senales detectadas:")
                for s in resultado.senales:
                    print(f"   - {s}")
            else:
                print("No se detectaron senales de riesgo.")
        except URLInvalidaError as e:
            print(f"\n[!] Error: {e}")

    def _opcion_historial(self):
        """Muestra todos los analisis guardados."""
        analisis = self._ctrl.obtener_historial()
        if not analisis:
            print("\nEl historial esta vacio.")
            return
        print(f"\n--- HISTORIAL ({len(analisis)} analisis) ---")
        for i, a in enumerate(analisis, 1):
            print(f"{i}. [{a['nivel_riesgo'].upper()}] {a['url']} "
                  f"({a['puntaje_total']} pts) - {a['fecha']}")