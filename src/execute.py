import tkinter as tk
from tkinter import messagebox, simpledialog
from functools import wraps

from usuarios import Usuario
from producto import Producto
from vehiculo import Vehiculo
from venta import Venta
from ordenCompra import OrdenCompra
from notaPedido import NotaPedido

def requiere_admin(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.current_user or self.current_user.rol != 'administrador':
            messagebox.showerror("Permisos", "Accion restringida: se requiere usuario administrador.")
            return
        return func(self, *args, **kwargs)
    return wrapper

def requiere_autenticacion(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            messagebox.showerror("Permisos", "Debe iniciar sesion para realizar esta accion.")
            return
        return func(self, *args, **kwargs)
    return wrapper

class PuntoVentaGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Punto de Venta - Refaccionaria")
        self.current_user = None
        
        self.output = tk.Listbox(self.master, width=100, height=20)
        self.output.pack(padx=10, pady=10)
        
        # ESTADO DEL USUARIO
        self.user_status = tk.Label(self.master, text="No autenticado", 
                                   font=("Arial", 10), fg="red")
        self.user_status.pack(pady=5)

        # MENU Principal
        self.menubar = tk.Menu(self.master)

        # Menu Usuarios
        self.menu_usuarios = tk.Menu(self.menubar, tearoff=0)
        self.menu_usuarios.add_command(label="Registrar Usuario", command=self.registrar_usuario)
        self.menu_usuarios.add_command(label="Listar Usuarios", command=self.listar_usuarios)
        self.menu_usuarios.add_command(label="Eliminar Usuario", command=self.eliminar_usuario)
        self.menubar.add_cascade(label="Usuarios", menu=self.menu_usuarios)

        # Productos
        self.menu_productos = tk.Menu(self.menubar, tearoff=0)
        self.menu_productos.add_command(label="Registrar Producto", command=self.registrar_producto)
        self.menu_productos.add_command(label="Listar Productos", command=self.listar_productos)
        self.menubar.add_cascade(label="Productos", menu=self.menu_productos)

        # Vehiculos
        self.menu_vehiculos = tk.Menu(self.menubar, tearoff=0)
        self.menu_vehiculos.add_command(label="Registrar Vehiculo", command=self.registrar_vehiculo)
        self.menu_vehiculos.add_command(label="Listar Vehiculos", command=self.listar_vehiculos)
        self.menubar.add_cascade(label="Vehiculos", menu=self.menu_vehiculos)

        # Ventas
        self.menu_ventas = tk.Menu(self.menubar, tearoff=0)
        self.menu_ventas.add_command(label="Crear Venta", command=self.crear_venta)
        self.menu_ventas.add_command(label="Listar Ventas", command=self.listar_ventas)
        self.menubar.add_cascade(label="Ventas", menu=self.menu_ventas)

        # Ordenes de compra
        self.menu_compras = tk.Menu(self.menubar, tearoff=0)
        self.menu_compras.add_command(label="Registrar Orden de Compra", command=self.registrar_compra)
        self.menu_compras.add_command(label="Listar Ordenes de Compra", command=self.listar_compras)
        self.menubar.add_cascade(label="Compras", menu=self.menu_compras)

        # Notas de productos faltantes
        self.menu_notas = tk.Menu(self.menubar, tearoff=0)
        self.menu_notas.add_command(label="Registrar Nota", command=self.registrar_nota)
        self.menu_notas.add_command(label="Listar Notas", command=self.listar_notas)
        self.menubar.add_cascade(label="Notas", menu=self.menu_notas)

        # Menu Archivo (Login/Logout)
        self.menu_archivo = tk.Menu(self.menubar, tearoff=0)
        self.menu_archivo.add_command(label="Cerrar Sesion", command=self.cerrar_sesion)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.salir)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)
        
        self.master.config(menu=self.menubar)
        # Deshabilitar menus hasta hacer login
        self.ajustar_menu_por_rol()        
        self.master.after(100, self.login_inicial)

    # SISTEMA DE LOGIN
    def login_inicial(self):
        # Verificar si hay usuarios en el sistema
        usuarios = Usuario.listar_todos()
        
        if not usuarios:
            # No hay usuarios
            self.crear_primer_admin()
            return
        
        tiene_cuenta = messagebox.askyesno("Bienvenido", "¿Ya tienes una cuenta en el sistema?")
        
        if not tiene_cuenta:
            # Permitir registro (solo vendedores)
            if self.registrar_usuario_publico():
                return
            else:
                messagebox.showinfo("Info", "Se solicitara inicio de sesion.")

        # Inicio de sesion (3 intentos)
        for intento in range(3):
            correo = simpledialog.askstring("Inicio de Sesion", "Correo electronico:")
            if correo is None:
                self.salir()
                return
                
            password = simpledialog.askstring("Inicio de Sesion", "Contrasena:", show='*')
            if password is None:
                self.salir()
                return

            usuario = Usuario.autenticar(correo.strip(), password)
            if usuario:
                self.current_user = usuario
                self.actualizar_estado_usuario()
                self.ajustar_menu_por_rol()
                messagebox.showinfo("Exito", f"Bienvenido, {usuario.nombre}!")
                return
            else:
                if intento < 2:
                    retry = messagebox.askretrycancel("Error", "Credenciales incorrectas. ¿Intentar de nuevo?")
                    if not retry:
                        if messagebox.askyesno("Registro", "¿Deseas registrarte como vendedor?"):
                            self.registrar_usuario_publico()
                        break
                else:
                    messagebox.showerror("Error", "Demasiados intentos fallidos.")        
        self.salir()
    
    def crear_primer_admin(self):
        """Primer usuario administrador del sistema"""
        messagebox.showinfo(
            "Primer Usuario", 
            "No hay usuarios en el sistema. Debes crear el primer usuario administrador."
        )
        
        while True:
            try:
                nombre = simpledialog.askstring("Primer Administrador", "Nombre completo:")
                if not nombre:
                    if messagebox.askyesno("Salir", "¿Deseas salir del sistema?"):
                        self.salir()
                        return
                    continue
                    
                correo = simpledialog.askstring("Primer Administrador", "Correo electronico:")
                if not correo:
                    continue
                    
                password = simpledialog.askstring("Primer Administrador", "Contrasena:", show='*')
                if not password:
                    continue

                codigo_admin = simpledialog.askstring(
                    "Codigo de Administrador", 
                    "Ingrese el codigo de administrador para crear el primer usuario:",
                    show='*'
                )
                
                if not codigo_admin:
                    continue

                # Crear el primer admin
                usuario = Usuario.crear(
                    nombre.strip(), 
                    correo.strip(), 
                    password, 
                    "administrador", 
                    codigo_admin
                )
                
                if usuario:
                    self.current_user = usuario
                    self.actualizar_estado_usuario()
                    self.ajustar_menu_por_rol()
                    messagebox.showinfo(
                        "Exito", 
                        f"Usuario administrador '{usuario.nombre}' creado exitosamente.\n\n"
                        f"Ahora puedes crear mas usuarios desde el menu Usuarios."
                    )
                    return True
                    
            except ValueError as e:
                messagebox.showerror("Error", f"Codigo incorrecto: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear usuario: {e}")
                if not messagebox.askyesno("Reintentar", "¿Intentar de nuevo?"):
                    self.salir()
                    return

    def registrar_usuario_publico(self):
        """Crear usuarios vendedor"""
        try:
            messagebox.showinfo(
                "Registro Publico", 
                "Solo puedes registrarte como VENDEDOR.\n\n"
                "Para crear usuarios administrador, un administrador existente "
                "debe hacerlo desde el menu Usuarios."
            )
            
            nombre = simpledialog.askstring("Registro - Vendedor", "Nombre completo:")
            if not nombre:
                return False
                
            correo = simpledialog.askstring("Registro - Vendedor", "Correo electronico:")
            if not correo:
                return False
                
            password = simpledialog.askstring("Registro - Vendedor", "Contrasena:", show='*')
            if not password:
                return False

            # Crea un usuario vendedor solo para vendedores
            usuario = Usuario.crear(nombre.strip(), correo.strip(), password, "vendedor")
            if usuario:
                self.current_user = usuario
                self.actualizar_estado_usuario()
                self.ajustar_menu_por_rol()
                messagebox.showinfo("Exito", f"Vendedor registrado: {usuario.nombre}")
                return True
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en registro: {e}")
            
        return False

    def actualizar_estado_usuario(self):
        if self.current_user:
            self.user_status.config(
                text=f"Usuario: {self.current_user.nombre} ({self.current_user.rol})", 
                fg="green"
            )
        else:
            self.user_status.config(text="No autenticado", fg="red")

    def ajustar_menu_por_rol(self):
        """Ajusta los menus segun el rol del usuario"""
        if not self.current_user:
            # Sin autenticacion admin
            for menu in [self.menu_usuarios, self.menu_productos, self.menu_vehiculos, 
                        self.menu_ventas, self.menu_compras, self.menu_notas]:
                menu.entryconfig(0, state="disabled")
            return

        if self.current_user.rol == 'administrador':
            # Admin: acceso completo
            for menu in [self.menu_usuarios, self.menu_productos, self.menu_vehiculos, 
                        self.menu_ventas, self.menu_compras, self.menu_notas]:
                menu.entryconfig(0, state="normal")
        else:
            # Vendedor: solo ventas y notas
            self.menu_usuarios.entryconfig(0, state="disabled")  # Registrar usuario
            self.menu_usuarios.entryconfig(2, state="disabled")  # Eliminar usuario
            self.menu_productos.entryconfig(0, state="disabled")  # Registrar producto
            self.menu_vehiculos.entryconfig(0, state="disabled")  # Registrar vehiculo
            self.menu_compras.entryconfig(0, state="disabled")   # Registrar orden compra
            
            # Habilitar ventas y notas para vendedores
            self.menu_ventas.entryconfig(0, state="normal")
            self.menu_notas.entryconfig(0, state="normal")

    def cerrar_sesion(self):
        self.current_user = None
        self.actualizar_estado_usuario()
        self.ajustar_menu_por_rol()
        self.login_inicial()

    def salir(self):
        self.master.destroy()

    # FUNCIONES CON CONTROL DE PERMISOS
    @requiere_admin
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
                codigo_admin = None
                if rol.get().strip().lower() == 'administrador':
                    codigo_admin = simpledialog.askstring("Codigo Admin", 
                                                        "Ingrese el codigo de administrador:", 
                                                        show='*')
                    if not codigo_admin:
                        messagebox.showerror("Error", "Se requiere codigo para administrador.")
                        return

                Usuario.crear(nombre.get(), correo.get(), password.get(), 
                             rol.get().strip().lower(), codigo_admin)
                messagebox.showinfo("Exito", "Usuario registrado.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    @requiere_autenticacion
    def listar_usuarios(self):
        self.output.delete(0, tk.END)
        usuarios = Usuario.listar_todos()
        if not usuarios:
            self.output.insert(tk.END, "No hay usuarios registrados.")
            return
            
        # Mostrar encabezados
        encabezado = f"{'ID':<5} {'NOMBRE':<30} {'CORREO':<30} {'ROL':<15}"
        self.output.insert(tk.END, encabezado)
        self.output.insert(tk.END, "-" * 85)
        
        # Mostrar cada usuario
        for u in usuarios:
            usuario_str = f"{u.id:<5} {u.nombre:<30} {u.correo if u.correo else 'N/A':<30} {u.rol:<15}"
            self.output.insert(tk.END, usuario_str)

    @requiere_admin
    def eliminar_usuario(self):
        # CORREGIDO: Pedir correo en lugar de nombre
        correo = simpledialog.askstring("Eliminar Usuario", "Correo del usuario a eliminar:")
        if not correo:
            return
            
        usuario = Usuario.buscar_por_correo(correo)
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return
            
        if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario '{usuario.nombre}'?"):
            try:
                usuario.eliminar()
                messagebox.showinfo("Exito", "Usuario eliminado.")
                self.listar_usuarios()  # Esto deberia funcionar ahora
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    @requiere_admin
    def registrar_producto(self):
        win = tk.Toplevel(self.master)
        win.title("Registrar Producto")

        labels = ["Nombre", "Marca", "Tipo (refaccion/accesorio)", 
                  "Categoria", "Version", "Precio Costo", "Precio Venta", "Existencias"]
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
                    entries["Categoria"].get(),
                    entries["Version"].get(),
                    float(entries["Precio Costo"].get()),
                    float(entries["Precio Venta"].get()),
                    int(entries["Existencias"].get())
                )
                messagebox.showinfo("Exito", "Producto agregado.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    @requiere_autenticacion
    def listar_productos(self):
        self.output.delete(0, tk.END)
        productos = Producto.listar_todos()
        for p in productos:
            self.output.insert(tk.END, str(p))

    @requiere_admin
    def registrar_vehiculo(self):
        win = tk.Toplevel(self.master)
        win.title("Registrar Vehiculo")

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
                messagebox.showinfo("Exito", "Vehiculo registrado.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    @requiere_autenticacion
    def listar_vehiculos(self):
        self.output.delete(0, tk.END)
        vehiculos = Vehiculo.listar_todos()
        for v in vehiculos:
            self.output.insert(tk.END, str(v))

    @requiere_autenticacion
    def crear_venta(self):
        win = tk.Toplevel(self.master)
        win.title("Crear Venta")

        tk.Label(win, text="ID Producto:").pack()
        id_producto = tk.Entry(win)
        id_producto.pack()

        tk.Label(win, text="Cantidad:").pack()
        cantidad = tk.Entry(win)
        cantidad.pack()

        def guardar():
            try:
                # Usar el usuario actual
                Venta.crear(
                    self.current_user.id,  # ID usuario del login
                    "2024-01-01",
                    int(id_producto.get()),
                    int(cantidad.get())
                )
                messagebox.showinfo("Exito", "Venta registrada.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Registrar Venta", command=guardar).pack()

    @requiere_autenticacion
    def listar_ventas(self):
        self.output.delete(0, tk.END)
        ventas = Venta.listar_todas()
        for v in ventas:
            self.output.insert(tk.END, str(v))

    @requiere_admin
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
                messagebox.showinfo("Exito", "Orden de compra registrada.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    @requiere_admin
    def listar_compras(self):
        self.output.delete(0, tk.END)
        compras = OrdenCompra.listar_todas()
        for c in compras:
            self.output.insert(tk.END, str(c))

    @requiere_autenticacion
    def registrar_nota(self):
        win = tk.Toplevel(self.master)
        win.title("Registrar Nota de Producto Faltante")

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
                # Usar el usuario actual
                NotaPedido.crear(
                    self.current_user.id,  # ID usuario del login
                    prod.get(),
                    det.get(),
                    fecha.get()
                )
                messagebox.showinfo("Exito", "Nota registrada.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    @requiere_autenticacion
    def listar_notas(self):
        self.output.delete(0, tk.END)
        notas = NotaPedido.listar_todas()
        for n in notas:
            self.output.insert(tk.END, str(n))

if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoVentaGUI(root)
    root.mainloop()