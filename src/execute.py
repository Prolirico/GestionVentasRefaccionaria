import tkinter as tk
from tkinter import messagebox

from usuarios import Usuario
from producto import Producto
from vehiculo import Vehiculo
from venta import Venta
from ordenCompra import OrdenCompra
from notaPedido import NotaPedido


class PuntoVentaGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Punto de Venta - Refaccionaria")

        # LISTBOX DE SALIDA
        self.output = tk.Listbox(self.master, width=100, height=20)
        self.output.pack(padx=10, pady=10)

        # MENU PRINCIPAL
        menubar = tk.Menu(self.master)

        # Menu Usuarios
        menu_usuarios = tk.Menu(menubar, tearoff=0)
        menu_usuarios.add_command(label="Registrar Usuario", command=self.registrar_usuario)
        menu_usuarios.add_command(label="Listar Usuarios", command=self.listar_usuarios)
        menubar.add_cascade(label="Usuarios", menu=menu_usuarios)

        # Productos
        menu_productos = tk.Menu(menubar, tearoff=0)
        menu_productos.add_command(label="Registrar Producto", command=self.registrar_producto)
        menu_productos.add_command(label="Listar Productos", command=self.listar_productos)
        menubar.add_cascade(label="Productos", menu=menu_productos)

        # Vehiculos
        menu_vehiculos = tk.Menu(menubar, tearoff=0)
        menu_vehiculos.add_command(label="Registrar Vehículo", command=self.registrar_vehiculo)
        menu_vehiculos.add_command(label="Listar Vehículos", command=self.listar_vehiculos)
        menubar.add_cascade(label="Vehículos", menu=menu_vehiculos)

        # Ventas
        menu_ventas = tk.Menu(menubar, tearoff=0)
        menu_ventas.add_command(label="Crear Venta", command=self.crear_venta)
        menu_ventas.add_command(label="Listar Ventas", command=self.listar_ventas)
        menubar.add_cascade(label="Ventas", menu=menu_ventas)

        # Ordenes de compra
        menu_compras = tk.Menu(menubar, tearoff=0)
        menu_compras.add_command(label="Registrar Orden de Compra", command=self.registrar_compra)
        menu_compras.add_command(label="Listar Órdenes de Compra", command=self.listar_compras)
        menubar.add_cascade(label="Compras", menu=menu_compras)

        # Notas de productos faltantes
        menu_notas = tk.Menu(menubar, tearoff=0)
        menu_notas.add_command(label="Registrar Nota", command=self.registrar_nota)
        menu_notas.add_command(label="Listar Notas", command=self.listar_notas)
        menubar.add_cascade(label="Notas", menu=menu_notas)

        self.master.config(menu=menubar)

    # FUNCIONES PARA USUARIOS
    def registrar_usuario(self):
        win = tk.Toplevel(self.master)
        win.title("Registrar Usuario")

        tk.Label(win, text="Nombre:").pack()
        nombre = tk.Entry(win)
        nombre.pack()

        tk.Label(win, text="Rol (vendedor/administrador):").pack()
        rol = tk.Entry(win)
        rol.pack()

        tk.Label(win, text="Correo:").pack()
        correo = tk.Entry(win)
        correo.pack()

        tk.Label(win, text="Password:").pack()
        password = tk.Entry(win, show="*")
        password.pack()

        def guardar():
            try:
                Usuario.crear(nombre.get(), rol.get(), correo.get(), password.get())
                messagebox.showinfo("Éxito", "Usuario registrado.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    def listar_usuarios(self):
        self.output.delete(0, tk.END)
        usuarios = Usuario.listar_todos()
        for u in usuarios:
            self.output.insert(tk.END, str(u))

    # PRODUCTOS
    def registrar_producto(self):
        win = tk.Toplevel(self.master)
        win.title("Registrar Producto")

        labels = ["Nombre", "Marca", "Tipo (refaccion/accesorio)", 
                  "Categoría", "Versión", "Precio Costo", "Precio Venta", "Existencias"]
        entries = {}

        for l in labels:
            tk.Label(win, text=l + ":").pack()
            e = tk.Entry(win)
            e.pack()
            entries[l] = e

        def guardar():
            try:
                Producto.crear(
                    entries["Nombre"].get(),
                    entries["Marca"].get(),
                    entries["Tipo (refaccion/accesorio)"].get(),
                    entries["Categoría"].get(),
                    entries["Versión"].get(),
                    float(entries["Precio Costo"].get()),
                    float(entries["Precio Venta"].get()),
                    int(entries["Existencias"].get())
                )
                messagebox.showinfo("Éxito", "Producto agregado.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    def listar_productos(self):
        self.output.delete(0, tk.END)
        productos = Producto.listar_todos()
        for p in productos:
            self.output.insert(tk.END, str(p))

    # VEHICULOS
    def registrar_vehiculo(self):
        win = tk.Toplevel(self.master)
        win.title("Registrar Vehículo")

        labels = ["Marca", "Modelo", "Año"]
        entries = {}

        for l in labels:
            tk.Label(win, text=l + ":").pack()
            e = tk.Entry(win)
            e.pack()
            entries[l] = e

        def guardar():
            try:
                Vehiculo.crear(
                    entries["Marca"].get(),
                    entries["Modelo"].get(),
                    int(entries["Año"].get())
                )
                messagebox.showinfo("Éxito", "Vehículo registrado.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    def listar_vehiculos(self):
        self.output.delete(0, tk.END)
        vehiculos = Vehiculo.listar_todos()
        for v in vehiculos:
            self.output.insert(tk.END, str(v))

    # VENTAS
    def crear_venta(self):
        win = tk.Toplevel(self.master)
        win.title("Crear Venta")

        tk.Label(win, text="ID Usuario:").pack()
        id_usuario = tk.Entry(win)
        id_usuario.pack()

        tk.Label(win, text="ID Producto:").pack()
        id_producto = tk.Entry(win)
        id_producto.pack()

        tk.Label(win, text="Cantidad:").pack()
        cantidad = tk.Entry(win)
        cantidad.pack()

        def guardar():
            try:
                Venta.crear(
                    int(id_usuario.get()),
                    int(id_producto.get()),
                    int(cantidad.get())
                )
                messagebox.showinfo("Éxito", "Venta registrada.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Registrar Venta", command=guardar).pack()

    def listar_ventas(self):
        self.output.delete(0, tk.END)
        ventas = Venta.listar_todas()
        for v in ventas:
            self.output.insert(tk.END, str(v))

    # ORDENES DE COMPRA
    def registrar_compra(self):
        win = tk.Toplevel(self.master)
        win.title("Registrar Orden de Compra")

        labels = ["ID Proveedor", "Fecha", "ID Producto", "Cantidad", "Precio Unitario", "Estado"]
        entries = {}

        for l in labels:
            tk.Label(win, text=l + ":").pack()
            e = tk.Entry(win)
            e.pack()
            entries[l] = e

        def guardar():
            try:
                OrdenCompra.crear(
                    int(entries["ID Proveedor"].get()),
                    entries["Fecha"].get(),
                    int(entries["ID Producto"].get()),
                    int(entries["Cantidad"].get()),
                    float(entries["Precio Unitario"].get()),
                    entries["Estado"].get()
                )
                messagebox.showinfo("Éxito", "Orden de compra registrada.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    def listar_compras(self):
        self.output.delete(0, tk.END)
        compras = OrdenCompra.listar_todas()
        for c in compras:
            self.output.insert(tk.END, str(c))

    # NOTAS DE PRODUCTOS FALTANTES
    def registrar_nota(self):
        win = tk.Toplevel(self.master)
        win.title("Registrar Nota de Producto Faltante")

        tk.Label(win, text="ID Usuario:").pack()
        id_usuario = tk.Entry(win)
        id_usuario.pack()

        tk.Label(win, text="Nombre Producto:").pack()
        prod = tk.Entry(win)
        prod.pack()

        tk.Label(win, text="Detalles:").pack()
        det = tk.Entry(win)
        det.pack()

        tk.Label(win, text="Fecha:").pack()
        fecha = tk.Entry(win)
        fecha.pack()

        def guardar():
            try:
                NotaPedido.crear(
                    int(id_usuario.get()),
                    prod.get(),
                    det.get(),
                    fecha.get()
                )
                messagebox.showinfo("Éxito", "Nota registrada.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    def listar_notas(self):
        self.output.delete(0, tk.END)
        notas = NotaPedido.listar_todas()
        for n in notas:
            self.output.insert(tk.END, str(n))

if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoVentaGUI(root)
    root.mainloop()
