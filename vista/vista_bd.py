"""
Vista del Entregable 4: pestanas CRUD sobre la base de datos + graficas.
- Pestana Reglas  : CRUD completo (crear, consultar, modificar, eliminar).
- Pestana URLs    : CRUD completo.
- Pestana Graficas: 2 graficas alimentadas desde la base de datos.

Manejo de errores: cualquier fallo de conexion se muestra al usuario con
un mensaje claro (messagebox), nunca con una traza tecnica en pantalla.

Se puede:
  a) Integrar en tu ventana existente:  agregar_pestanas(notebook)
  b) Ejecutar solo para probar/capturar:  python -m vista.vista_bd
"""
import tkinter as tk
from tkinter import ttk, messagebox

from datos.conexion import ErrorConexionBD
from datos.regla_dao import ReglaDAO
from datos.url_dao import UrlDAO
from datos.consultas_dao import ConsultasDAO

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def _mostrar_error(exc):
    """Traduce cualquier excepcion a un mensaje comprensible para el usuario."""
    if isinstance(exc, ErrorConexionBD):
        messagebox.showerror("Error de conexion", str(exc))
    else:
        messagebox.showerror(
            "Error",
            "Ocurrio un problema al procesar la operacion. "
            "Intente nuevamente."
        )


# ======================================================================
#  PESTANA: GESTION DE REGLAS (CRUD)
# ======================================================================
class GestionReglasFrame(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padding=10)
        self.dao = ReglaDAO()
        self._construir()
        self.refrescar()

    def _construir(self):
        # Formulario
        form = ttk.LabelFrame(self, text="Datos de la regla", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.e_nombre = ttk.Entry(form, width=30)
        self.e_nombre.grid(row=0, column=1, padx=5, pady=3)

        ttk.Label(form, text="Peso:").grid(row=0, column=2, sticky="w")
        self.e_peso = ttk.Entry(form, width=8)
        self.e_peso.grid(row=0, column=3, padx=5, pady=3)

        ttk.Label(form, text="Descripcion:").grid(row=1, column=0, sticky="w")
        self.e_desc = ttk.Entry(form, width=60)
        self.e_desc.grid(row=1, column=1, columnspan=3, padx=5, pady=3, sticky="w")

        # Botones CRUD
        botones = ttk.Frame(self)
        botones.pack(fill="x", pady=8)
        ttk.Button(botones, text="Crear", command=self.crear).pack(side="left", padx=3)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=3)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=3)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=3)

        # Tabla
        cols = ("id", "nombre", "peso", "descripcion")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c, ancho in zip(cols, (40, 160, 60, 400)):
            self.tabla.heading(c, text=c.capitalize())
            self.tabla.column(c, width=ancho)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

    def refrescar(self):
        try:
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)
            for r in self.dao.listar():
                self.tabla.insert("", "end", values=(r[0], r[1], r[2], r[3]))
        except Exception as e:
            _mostrar_error(e)

    def _al_seleccionar(self, _evento):
        sel = self.tabla.focus()
        if not sel:
            return
        v = self.tabla.item(sel, "values")
        self.limpiar()
        self.e_nombre.insert(0, v[1])
        self.e_peso.insert(0, v[2])
        self.e_desc.insert(0, v[3])

    def _id_seleccionado(self):
        sel = self.tabla.focus()
        if not sel:
            messagebox.showwarning("Atencion", "Seleccione una regla de la tabla.")
            return None
        return self.tabla.item(sel, "values")[0]

    def crear(self):
        try:
            peso = int(self.e_peso.get())
            self.dao.crear(self.e_nombre.get(), peso, self.e_desc.get())
            self.limpiar()
            self.refrescar()
            messagebox.showinfo("Listo", "Regla creada correctamente.")
        except ValueError:
            messagebox.showwarning("Atencion", "El peso debe ser un numero entero.")
        except Exception as e:
            _mostrar_error(e)

    def actualizar(self):
        idr = self._id_seleccionado()
        if idr is None:
            return
        try:
            peso = int(self.e_peso.get())
            self.dao.actualizar(idr, self.e_nombre.get(), peso, self.e_desc.get())
            self.limpiar()
            self.refrescar()
            messagebox.showinfo("Listo", "Regla actualizada correctamente.")
        except ValueError:
            messagebox.showwarning("Atencion", "El peso debe ser un numero entero.")
        except Exception as e:
            _mostrar_error(e)

    def eliminar(self):
        idr = self._id_seleccionado()
        if idr is None:
            return
        if not messagebox.askyesno("Confirmar", "Eliminar la regla seleccionada?"):
            return
        try:
            self.dao.eliminar(idr)
            self.limpiar()
            self.refrescar()
            messagebox.showinfo("Listo", "Regla eliminada correctamente.")
        except Exception as e:
            _mostrar_error(e)

    def limpiar(self):
        self.e_nombre.delete(0, "end")
        self.e_peso.delete(0, "end")
        self.e_desc.delete(0, "end")


# ======================================================================
#  PESTANA: GESTION DE URLS (CRUD)
# ======================================================================
class GestionUrlsFrame(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padding=10)
        self.dao = UrlDAO()
        self._construir()
        self.refrescar()

    def _construir(self):
        form = ttk.LabelFrame(self, text="Datos de la URL", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Direccion:").grid(row=0, column=0, sticky="w")
        self.e_dir = ttk.Entry(form, width=55)
        self.e_dir.grid(row=0, column=1, columnspan=3, padx=5, pady=3, sticky="w")

        ttk.Label(form, text="Dominio:").grid(row=1, column=0, sticky="w")
        self.e_dom = ttk.Entry(form, width=30)
        self.e_dom.grid(row=1, column=1, padx=5, pady=3)

        ttk.Label(form, text="Longitud:").grid(row=1, column=2, sticky="w")
        self.e_lon = ttk.Entry(form, width=8)
        self.e_lon.grid(row=1, column=3, padx=5, pady=3)

        botones = ttk.Frame(self)
        botones.pack(fill="x", pady=8)
        ttk.Button(botones, text="Crear", command=self.crear).pack(side="left", padx=3)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=3)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=3)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=3)

        cols = ("id", "direccion", "dominio", "longitud")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c, ancho in zip(cols, (40, 380, 200, 70)):
            self.tabla.heading(c, text=c.capitalize())
            self.tabla.column(c, width=ancho)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

    def refrescar(self):
        try:
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)
            for u in self.dao.listar():
                self.tabla.insert("", "end", values=(u[0], u[1], u[2], u[3]))
        except Exception as e:
            _mostrar_error(e)

    def _al_seleccionar(self, _evento):
        sel = self.tabla.focus()
        if not sel:
            return
        v = self.tabla.item(sel, "values")
        self.limpiar()
        self.e_dir.insert(0, v[1])
        self.e_dom.insert(0, v[2])
        self.e_lon.insert(0, v[3])

    def _id_seleccionado(self):
        sel = self.tabla.focus()
        if not sel:
            messagebox.showwarning("Atencion", "Seleccione una URL de la tabla.")
            return None
        return self.tabla.item(sel, "values")[0]

    def crear(self):
        try:
            longitud = int(self.e_lon.get())
            self.dao.crear(self.e_dir.get(), self.e_dom.get(), longitud)
            self.limpiar()
            self.refrescar()
            messagebox.showinfo("Listo", "URL creada correctamente.")
        except ValueError:
            messagebox.showwarning("Atencion", "La longitud debe ser un numero entero.")
        except Exception as e:
            _mostrar_error(e)

    def actualizar(self):
        idu = self._id_seleccionado()
        if idu is None:
            return
        try:
            longitud = int(self.e_lon.get())
            self.dao.actualizar(idu, self.e_dir.get(), self.e_dom.get(), longitud)
            self.limpiar()
            self.refrescar()
            messagebox.showinfo("Listo", "URL actualizada correctamente.")
        except ValueError:
            messagebox.showwarning("Atencion", "La longitud debe ser un numero entero.")
        except Exception as e:
            _mostrar_error(e)

    def eliminar(self):
        idu = self._id_seleccionado()
        if idu is None:
            return
        if not messagebox.askyesno("Confirmar", "Eliminar la URL seleccionada?"):
            return
        try:
            self.dao.eliminar(idu)
            self.limpiar()
            self.refrescar()
            messagebox.showinfo("Listo", "URL eliminada correctamente.")
        except Exception as e:
            _mostrar_error(e)

    def limpiar(self):
        self.e_dir.delete(0, "end")
        self.e_dom.delete(0, "end")
        self.e_lon.delete(0, "end")


# ======================================================================
#  PESTANA: GRAFICAS DESDE LA BASE DE DATOS
# ======================================================================
class GraficasFrame(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padding=10)
        self.consultas = ConsultasDAO()
        ttk.Button(self, text="Actualizar graficas",
                   command=self.dibujar).pack(pady=5)
        self.contenedor = ttk.Frame(self)
        self.contenedor.pack(fill="both", expand=True)
        self.canvas = None
        self.dibujar()

    def dibujar(self):
        try:
            reglas = self.consultas.reglas_mas_activadas()
            niveles = self.consultas.analisis_por_nivel()
        except Exception as e:
            _mostrar_error(e)
            return

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        figura = Figure(figsize=(9, 4), dpi=100)

        # Grafica 1: reglas mas activadas (barras)
        ax1 = figura.add_subplot(1, 2, 1)
        if reglas:
            nombres = [r[0] for r in reglas]
            valores = [r[1] for r in reglas]
            ax1.barh(nombres, valores, color="#c0392b")
            ax1.set_title("Reglas mas activadas")
            ax1.invert_yaxis()
        else:
            ax1.set_title("Sin datos")

        # Grafica 2: analisis por nivel (pastel)
        ax2 = figura.add_subplot(1, 2, 2)
        datos = [n for n in niveles if n[1] > 0]
        if datos:
            ax2.pie([d[1] for d in datos], labels=[d[0] for d in datos],
                    autopct="%1.0f%%", startangle=90)
            ax2.set_title("Analisis por nivel de riesgo")
        else:
            ax2.set_title("Sin datos")

        figura.tight_layout()
        self.canvas = FigureCanvasTkAgg(figura, master=self.contenedor)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


# ======================================================================
#  INTEGRACION Y EJECUCION
# ======================================================================
def agregar_pestanas(notebook):
    """Agrega las 3 pestanas del E4 a un ttk.Notebook existente."""
    notebook.add(GestionReglasFrame(notebook), text="Gestion Reglas")
    notebook.add(GestionUrlsFrame(notebook), text="Gestion URLs")
    notebook.add(GraficasFrame(notebook), text="Graficas BD")


if __name__ == "__main__":
    # Permite ejecutar con:  python -m vista.vista_bd   (desde la raiz)
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    ventana = tk.Tk()
    ventana.title("Detector de Phishing - Gestion de datos (E4)")
    ventana.geometry("980x640")
    nb = ttk.Notebook(ventana)
    nb.pack(fill="both", expand=True)
    agregar_pestanas(nb)
    ventana.mainloop()
