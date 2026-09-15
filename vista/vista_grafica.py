"""
Vista grafica (GUI) con Tkinter.
Reemplaza el menu de consola por una interfaz de ventanas con pestañas.
Usa el MISMO controlador del Entregable 2: la logica del modelo NO cambia.
Incluye dos graficas de Matplotlib incrustadas en la ventana.
"""
import tkinter as tk
from tkinter import ttk
from controlador.analizador_controller import AnalizadorController
from modelo.excepciones import URLInvalidaError
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class VistaGrafica:
    # Paleta de colores (buen contraste para accesibilidad)
    COLOR_FONDO = "#2B2B2B"
    COLOR_PANEL = "#3C3F41"
    COLOR_TEXTO = "#FFFFFF"
    COLOR_ACENTO = "#4A7DBF"
    COLOR_ERROR = "#E74C3C"

    # Colores por nivel de riesgo
    COLORES_RIESGO = {
        "segura": "#27AE60",      # verde
        "sospechosa": "#E0A93B",  # naranja
        "peligrosa": "#C0392B",   # rojo
    }

    def __init__(self):
        self._ctrl = AnalizadorController()

        self._root = tk.Tk()
        self._root.title("Detector Heuristico de Phishing en URLs")
        self._root.geometry("780x640")
        self._root.configure(bg=self.COLOR_FONDO)

        self._construir_encabezado()
        self._construir_pestanas()
        self._construir_aviso()

    # ============================================================
    #  ENCABEZADO
    # ============================================================
    def _construir_encabezado(self):
        titulo = tk.Label(
            self._root,
            text="Detector Heuristico de Phishing",
            font=("Segoe UI", 18, "bold"),
            bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO, pady=12
        )
        titulo.pack(fill="x")

    # ============================================================
    #  PESTAÑAS (NOTEBOOK)
    # ============================================================
    def _construir_pestanas(self):
        self._notebook = ttk.Notebook(self._root)

        self._tab_analisis = tk.Frame(self._notebook, bg=self.COLOR_PANEL)
        self._tab_historial = tk.Frame(self._notebook, bg=self.COLOR_PANEL)
        self._tab_estadisticas = tk.Frame(self._notebook, bg=self.COLOR_PANEL)

        self._notebook.add(self._tab_analisis, text="  Analizar URL  ")
        self._notebook.add(self._tab_historial, text="  Historial  ")
        self._notebook.add(self._tab_estadisticas, text="  Estadisticas  ")
        self._notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._construir_tab_analisis()
        self._construir_tab_historial()
        self._construir_tab_estadisticas()

    # ============================================================
    #  PESTAÑA 1: ANALISIS
    # ============================================================
    def _construir_tab_analisis(self):
        cont = tk.Frame(self._tab_analisis, bg=self.COLOR_PANEL)
        cont.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(cont, text="Ingrese la URL a analizar:",
                 font=("Segoe UI", 11), bg=self.COLOR_PANEL,
                 fg=self.COLOR_TEXTO, anchor="w").pack(fill="x", pady=(0, 6))

        self._entrada_url = tk.Entry(
            cont, font=("Segoe UI", 11), bg="#1E1E1E",
            fg=self.COLOR_TEXTO, insertbackground=self.COLOR_TEXTO,
            relief="flat", highlightthickness=2,
            highlightbackground="#555555", highlightcolor=self.COLOR_ACENTO
        )
        self._entrada_url.pack(fill="x", ipady=8)
        self._entrada_url.bind("<Return>", lambda e: self._on_analizar())
        self._entrada_url.focus_set()  # foco inicial en el campo (accesibilidad)

        btn = tk.Button(
            cont, text="Analizar URL", font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_ACENTO, fg=self.COLOR_TEXTO, relief="flat",
            activebackground="#3A6DAF", cursor="hand2",
            command=self._on_analizar
        )
        btn.pack(fill="x", pady=12, ipady=6)

        self._lbl_mensaje = tk.Label(
            cont, text="", font=("Segoe UI", 10),
            bg=self.COLOR_PANEL, fg=self.COLOR_ERROR, anchor="w"
        )
        self._lbl_mensaje.pack(fill="x")

        self._frame_resultado = tk.Frame(cont, bg=self.COLOR_PANEL)
        self._frame_resultado.pack(fill="both", expand=True, pady=(10, 0))

    def _on_analizar(self):
        """Callback del boton: valida, llama al controlador y muestra el resultado."""
        self._lbl_mensaje.config(text="")
        for w in self._frame_resultado.winfo_children():
            w.destroy()

        direccion = self._entrada_url.get().strip()

        if not direccion:
            self._entrada_url.config(highlightbackground=self.COLOR_ERROR,
                                     highlightcolor=self.COLOR_ERROR)
            self._lbl_mensaje.config(text="[!] El campo no puede estar vacio.")
            return

        try:
            resultado = self._ctrl.analizar_url(direccion)
            self._entrada_url.config(highlightbackground="#555555",
                                     highlightcolor=self.COLOR_ACENTO)
            self._mostrar_resultado(resultado)
            self._cargar_tabla()
            self._dibujar_graficas()
        except URLInvalidaError as e:
            self._entrada_url.config(highlightbackground=self.COLOR_ERROR,
                                     highlightcolor=self.COLOR_ERROR)
            self._lbl_mensaje.config(text=f"[!] {e}")

    def _mostrar_resultado(self, resultado):
        """Muestra el veredicto con color segun el nivel de riesgo."""
        color = self.COLORES_RIESGO.get(resultado.nivel_riesgo, self.COLOR_TEXTO)

        banner = tk.Label(
            self._frame_resultado,
            text=f"  {resultado.nivel_riesgo.upper()}  -  {resultado.puntaje_total} pts",
            font=("Segoe UI", 16, "bold"),
            bg=color, fg="#FFFFFF", pady=12
        )
        banner.pack(fill="x", pady=(6, 10))

        tk.Label(self._frame_resultado, text=f"URL: {resultado.url}",
                 font=("Segoe UI", 10), bg=self.COLOR_PANEL,
                 fg=self.COLOR_TEXTO, anchor="w", wraplength=700,
                 justify="left").pack(fill="x")

        if resultado.senales:
            tk.Label(self._frame_resultado, text="Senales detectadas:",
                     font=("Segoe UI", 10, "bold"), bg=self.COLOR_PANEL,
                     fg=self.COLOR_TEXTO, anchor="w").pack(fill="x", pady=(8, 2))
            for s in resultado.senales:
                tk.Label(self._frame_resultado, text=f"   - {s}",
                         font=("Segoe UI", 10), bg=self.COLOR_PANEL,
                         fg="#DDDDDD", anchor="w").pack(fill="x")
        else:
            tk.Label(self._frame_resultado,
                     text="No se detectaron senales de riesgo.",
                     font=("Segoe UI", 10), bg=self.COLOR_PANEL,
                     fg="#DDDDDD", anchor="w").pack(fill="x", pady=(8, 0))

    # ============================================================
    #  PESTAÑA 2: HISTORIAL (tabla con filtro y ordenamiento)
    # ============================================================
    def _construir_tab_historial(self):
        cont = tk.Frame(self._tab_historial, bg=self.COLOR_PANEL)
        cont.pack(fill="both", expand=True, padx=15, pady=15)

        barra = tk.Frame(cont, bg=self.COLOR_PANEL)
        barra.pack(fill="x", pady=(0, 10))

        tk.Label(barra, text="Filtrar por nivel:", font=("Segoe UI", 10),
                 bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO).pack(side="left", padx=(0, 8))

        self._filtro_nivel = ttk.Combobox(
            barra, values=["Todas", "segura", "sospechosa", "peligrosa"],
            state="readonly", width=15
        )
        self._filtro_nivel.set("Todas")
        self._filtro_nivel.pack(side="left")
        self._filtro_nivel.bind("<<ComboboxSelected>>", lambda e: self._cargar_tabla())

        tk.Button(barra, text="Actualizar", font=("Segoe UI", 9),
                  bg=self.COLOR_ACENTO, fg=self.COLOR_TEXTO, relief="flat",
                  cursor="hand2", command=self._cargar_tabla).pack(side="right")

        columnas = ("url", "nivel", "puntaje", "fecha")
        self._tabla = ttk.Treeview(cont, columns=columnas, show="headings", height=12)

        encabezados = {"url": "URL", "nivel": "Nivel", "puntaje": "Puntaje", "fecha": "Fecha"}
        anchos = {"url": 340, "nivel": 110, "puntaje": 80, "fecha": 130}
        for col in columnas:
            self._tabla.heading(col, text=encabezados[col],
                                command=lambda c=col: self._ordenar_tabla(c, False))
            self._tabla.column(col, width=anchos[col], anchor="w")

        self._tabla.pack(fill="both", expand=True, side="left")

        scroll = ttk.Scrollbar(cont, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        self._cargar_tabla()

    def _cargar_tabla(self):
        """Llena la tabla con el historial, aplicando el filtro seleccionado."""
        for fila in self._tabla.get_children():
            self._tabla.delete(fila)

        filtro = self._filtro_nivel.get()
        analisis = self._ctrl.obtener_historial()

        for a in analisis:
            if filtro != "Todas" and a["nivel_riesgo"] != filtro:
                continue
            self._tabla.insert("", "end", values=(
                a["url"], a["nivel_riesgo"].upper(),
                a["puntaje_total"], a["fecha"]
            ))

    def _ordenar_tabla(self, columna, descendente):
        """Ordena la tabla por la columna clicada."""
        datos = [(self._tabla.set(f, columna), f) for f in self._tabla.get_children()]
        try:
            datos.sort(key=lambda t: int(t[0]), reverse=descendente)
        except ValueError:
            datos.sort(key=lambda t: t[0].lower(), reverse=descendente)
        for indice, (_, f) in enumerate(datos):
            self._tabla.move(f, "", indice)
        self._tabla.heading(columna,
                            command=lambda: self._ordenar_tabla(columna, not descendente))

    # ============================================================
    #  PESTAÑA 3: ESTADISTICAS (2 graficas de Matplotlib)
    # ============================================================
    def _construir_tab_estadisticas(self):
        cont = tk.Frame(self._tab_estadisticas, bg=self.COLOR_PANEL)
        cont.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(cont, text="Actualizar graficas", font=("Segoe UI", 9),
                  bg=self.COLOR_ACENTO, fg=self.COLOR_TEXTO, relief="flat",
                  cursor="hand2", command=self._dibujar_graficas).pack(pady=(0, 8))

        self._frame_graficas = tk.Frame(cont, bg=self.COLOR_PANEL)
        self._frame_graficas.pack(fill="both", expand=True)

        self._dibujar_graficas()

    def _dibujar_graficas(self):
        """Crea las dos figuras con los datos reales del historial."""
        for w in self._frame_graficas.winfo_children():
            w.destroy()

        stats = self._ctrl.obtener_estadisticas()
        niveles = stats["niveles"]
        reglas = stats["reglas"]

        fig = Figure(figsize=(7, 3.4), dpi=100, facecolor="#3C3F41")

        # Grafica 1: pastel de distribucion de veredictos
        ax1 = fig.add_subplot(1, 2, 1)
        etiquetas = [k for k, v in niveles.items() if v > 0]
        valores = [v for v in niveles.values() if v > 0]
        colores = {"segura": "#27AE60", "sospechosa": "#E0A93B", "peligrosa": "#C0392B"}
        cols = [colores[k] for k in etiquetas]

        if valores:
            ax1.pie(valores, labels=etiquetas, autopct="%1.0f%%",
                    colors=cols, textprops={"color": "white", "fontsize": 8})
            ax1.set_title("Distribucion de veredictos", color="white", fontsize=10)
        else:
            ax1.text(0.5, 0.5, "Sin datos", ha="center", color="white")

        # Grafica 2: barras de reglas mas activadas
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.set_facecolor("#3C3F41")
        if reglas:
            nombres = list(reglas.keys())
            cuentas = list(reglas.values())
            cortos = [n.split()[0] for n in nombres]
            ax2.barh(cortos, cuentas, color="#4A7DBF")
            ax2.set_title("Reglas mas activadas", color="white", fontsize=10)
            ax2.tick_params(colors="white", labelsize=7)
            for spine in ax2.spines.values():
                spine.set_color("#777777")
        else:
            ax2.text(0.5, 0.5, "Sin datos", ha="center", color="white")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self._frame_graficas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ============================================================
    #  AVISO DE USO RESPONSABLE
    # ============================================================
    def _construir_aviso(self):
        aviso = tk.Label(
            self._root,
            text=("Uso responsable: esta herramienta realiza analisis estatico "
                  "de URLs (no visita ni ataca sitios). Fines educativos y defensivos."),
            font=("Segoe UI", 8), bg=self.COLOR_FONDO, fg="#AAAAAA",
            wraplength=760, justify="center", pady=6
        )
        aviso.pack(fill="x", side="bottom")

    def iniciar(self):
        self._root.mainloop()