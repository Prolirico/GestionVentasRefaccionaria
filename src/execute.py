import tkinter as tk
from tkinter import messagebox, simpledialog

from usuarios import Usuario
from producto import Producto
from vehiculo import Vehiculo
from venta import Venta
from ordenCompra import OrdenCompra
from notaPedido import NotaPedido

current_user = None

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
        self.menu_vehiculos.add_command(label="Registrar Vehículo", command=self.registrar_vehiculo)
        self.menu_vehiculos.add_command(label="Listar Vehículos", command=self.listar_vehiculos)
        self.menubar.add_cascade(label="Vehículos", menu=self.menu_vehiculos)

        # Ventas
        self.menu_ventas = tk.Menu(self.menubar, tearoff=0)
        self.menu_ventas.add_command(label="Crear Venta", command=self.crear_venta)
        self.menu_ventas.add_command(label="Listar Ventas", command=self.listar_ventas)
        self.menubar.add_cascade(label="Ventas", menu=self.menu_ventas)

        # Ordenes de compra
        self.menu_compras = tk.Menu(self.menubar, tearoff=0)
        self.menu_compras.add_command(label="Registrar Orden de Compra", command=self.registrar_compra)
        self.menu_compras.add_command(label="Listar Órdenes de Compra", command=self.listar_compras)
        self.menubar.add_cascade(label="Compras", menu=self.menu_compras)

        # Notas de productos faltantes
        self.menu_notas = tk.Menu(self.menubar, tearoff=0)
        self.menu_notas.add_command(label="Registrar Nota", command=self.registrar_nota)
        self.menu_notas.add_command(label="Listar Notas", command=self.listar_notas)
        self.menubar.add_cascade(label="Notas", menu=self.menu_notas)

        # Menu Archivo (Login/Logout)
        self.menu_archivo = tk.Menu(self.menubar, tearoff=0)
        self.menu_archivo.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.salir)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.master.config(menu=self.menubar)
        # Deshabilitar menus hasta hacer login
        self.ajustar_menu_por_rol()        
        self.master.after(100, self.login_inicial)

    @staticmethod
    def requiere_admin(func):
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'current_user') or not self.current_user or self.current_user.rol != 'administrador':
                messagebox.showerror("Permisos", "Acción restringida: se requiere usuario administrador.")
                return
            return func(self, *args, **kwargs)
        return wrapper

    def requiere_autenticacion(func):
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                messagebox.showerror("Permisos", "Debe iniciar sesión para realizar esta acción.")
                return
            return func(*args, **kwargs)
        return wrapper

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
                messagebox.showinfo("Info", "Se solicitará inicio de sesión.")

        # Inicio de sesion (3 intentos)
        for intento in range(3):
            correo = simpledialog.askstring("Inicio de Sesión", "Correo electrónico:")
            if correo is None:
                self.salir()
                return
                
            password = simpledialog.askstring("Inicio de Sesión", "Contraseña:", show='*')
            if password is None:
                self.salir()
                return

            usuario = Usuario.autenticar(correo.strip(), password)
            if usuario:
                self.current_user = usuario
                self.actualizar_estado_usuario()
                self.ajustar_menu_por_rol()
                messagebox.showinfo("Éxito", f"Bienvenido, {usuario.nombre}!")
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
                    
                correo = simpledialog.askstring("Primer Administrador", "Correo electrónico:")
                if not correo:
                    continue
                    
                password = simpledialog.askstring("Primer Administrador", "Contraseña:", show='*')
                if not password:
                    continue

                codigo_admin = simpledialog.askstring(
                    "Código de Administrador", 
                    "Ingrese el código de administrador para crear el primer usuario:",
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
                        "Éxito", 
                        f"Usuario administrador '{usuario.nombre}' creado exitosamente.\n\n"
                        f"Ahora puedes crear más usuarios desde el menú Usuarios."
                    )
                    return True
                    
            except ValueError as e:
                messagebox.showerror("Error", f"Código incorrecto: {e}")
                # No salir, permitir reintentar
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear usuario: {e}")
                if not messagebox.askyesno("Reintentar", "¿Intentar de nuevo?"):
                    self.salir()
                    return


    def registrar_usuario_publico(self):
        """Registro público que solo permite crear usuarios vendedor"""
        try:
            messagebox.showinfo(
                "Registro Público", 
                "Solo puedes registrarte como VENDEDOR.\n\n"
                "Para crear usuarios administrador, un administrador existente "
                "debe hacerlo desde el menú Usuarios."
            )
            
            nombre = simpledialog.askstring("Registro - Vendedor", "Nombre completo:")
            if not nombre:
                return False
                
            correo = simpledialog.askstring("Registro - Vendedor", "Correo electrónico:")
            if not correo:
                return False
                
            password = simpledialog.askstring("Registro - Vendedor", "Contraseña:", show='*')
            if not password:
                return False

            # Crea un usuario vendedor solo para vendedores
            usuario = Usuario.crear(nombre.strip(), correo.strip(), password, "vendedor")
            if usuario:
                self.current_user = usuario
                self.actualizar_estado_usuario()
                self.ajustar_menu_por_rol()
                messagebox.showinfo("Éxito", f"Vendedor registrado: {usuario.nombre}")
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
        """Ajusta los menús según el rol del usuario"""
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
            self.menu_vehiculos.entryconfig(0, state="disabled")  # Registrar vehículo
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
                    codigo_admin = simpledialog.askstring("Código Admin", 
                                                        "Ingrese el código de administrador:", 
                                                        show='*')
                    if not codigo_admin:
                        messagebox.showerror("Error", "Se requiere código para administrador.")
                        return

                Usuario.crear(nombre.get(), correo.get(), password.get(), 
                             rol.get().strip().lower(), codigo_admin)
                messagebox.showinfo("Éxito", "Usuario registrado.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack()

    @requiere_autenticacion
    def listar_usuarios(self):
        self.output.delete(0, tk.END)
        usuarios = Usuario.listar_todos()
        for u in usuarios:
            self.output.insert(tk.END, str(u))

    @requiere_admin
    def eliminar_usuario(self):
        nombre = simpledialog.askstring("Eliminar Usuario", "Nombre del usuario a eliminar:")
        if not nombre:
            return
            
        usuario = Usuario.buscar_por_correo(nombre)
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return
            
        if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario '{usuario.nombre}'?"):
            try:
                usuario.eliminar()
                messagebox.showinfo("Éxito", "Usuario eliminado.")
                self.listar_usuarios()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    @requiere_admin
    def registrar_producto(self):
        win = tk.Toplevel(self.master)

    @requiere_autenticacion
    def listar_productos(self):
        self.output.delete(0, tk.END)

    @requiere_admin
    def registrar_vehiculo(self):
        win = tk.Toplevel(self.master)

    @requiere_autenticacion
    def listar_vehiculos(self):
        self.output.delete(0, tk.END)

    @requiere_autenticacion
    def crear_venta(self):
        win = tk.Toplevel(self.master)

    @requiere_autenticacion
    def listar_ventas(self):
        self.output.delete(0, tk.END)

    @requiere_admin
    def registrar_compra(self):
        win = tk.Toplevel(self.master)

    @requiere_admin
    def listar_compras(self):
        self.output.delete(0, tk.END)

    @requiere_autenticacion
    def registrar_nota(self):
        win = tk.Toplevel(self.master)

    @requiere_autenticacion
    def listar_notas(self):
        self.output.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoVentaGUI(root)
    root.mainloop()