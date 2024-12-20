import tkinter as tk
from tkinter import messagebox
import os

def registrar_usuario():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if not usuario or not contrasena:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r") as archivo:
            for linea in archivo:
                usuario_existente, _ = linea.strip().split(",")
                if usuario == usuario_existente:
                    messagebox.showerror("Error", "El usuario ya existe.")
                    return

    with open("usuarios.txt", "a") as archivo:
        archivo.write(f"{usuario},{contrasena}\n")
    messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
    ventana_registro.destroy()

def iniciar_sesion():
    usuario = entry_usuario_login.get()
    contrasena = entry_contrasena_login.get()
    if not usuario or not contrasena:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r") as archivo:
            for linea in archivo:
                usuario_existente, contrasena_existente = linea.strip().split(",")
                if usuario == usuario_existente and contrasena == contrasena_existente:
                    messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                    ventana_login.destroy()
                    mostrar_menu_principal()
                    return

    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def mostrar_registro():
    global ventana_registro, entry_usuario, entry_contrasena

    ventana_registro = tk.Toplevel(ventana_login)
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("300x250")

    tk.Label(ventana_registro, text="Usuario:").pack(pady=5)
    entry_usuario = tk.Entry(ventana_registro)
    entry_usuario.pack(pady=5)

    tk.Label(ventana_registro, text="Contraseña:").pack(pady=5)
    entry_contrasena = tk.Entry(ventana_registro, show="*")
    entry_contrasena.pack(pady=5)

    tk.Button(ventana_registro, text="Registrar", command=registrar_usuario).pack(pady=10)

def dibujar_comida(canvas, tipo, x, y):
    if tipo == "hamburguesa":
        canvas.create_oval(x, y, x+80, y+40, fill="brown")  # Pan superior
        canvas.create_rectangle(x, y+20, x+80, y+50, fill="green")  # Lechuga
        canvas.create_rectangle(x, y+50, x+80, y+70, fill="red")  # Carne
        canvas.create_oval(x, y+60, x+80, y+100, fill="yellow")  # Pan inferior
    elif tipo == "pizza":
        canvas.create_polygon(x, y, x+40, y+100, x-40, y+100, fill="gold")  # Base
        canvas.create_oval(x-20, y+30, x+20, y+70, fill="red")  # Salsa
        canvas.create_oval(x-10, y+40, x+10, y+60, fill="white")  # Queso
    elif tipo == "bebida":
        canvas.create_rectangle(x, y, x+40, y+100, fill="blue")  # Vaso
        canvas.create_rectangle(x+15, y-20, x+25, y, fill="white")  # Popote

def mostrar_menu_principal():
    # Ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Pedido de Comida Rápida")
    ventana_principal.geometry("500x600")
    ventana_principal.resizable(False, False)

    # Variables
    cant_burger = tk.StringVar(value="0")
    cant_pizza = tk.StringVar(value="0")
    cant_bebida = tk.StringVar(value="0")
    carrito = []

    def agregar_al_carrito(item, cantidad, precio):
        try:
            cantidad = int(cantidad)
            if cantidad > 0:
                carrito.append((item, cantidad, precio * cantidad))
                messagebox.showinfo("Carrito", f"Agregado {cantidad} {item}(s) al carrito.")
            else:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese una cantidad válida.")

    def ver_carrito():
        if not carrito:
            messagebox.showinfo("Carrito", "El carrito está vacío.")
            return

        carrito_ventana = tk.Toplevel(ventana_principal)
        carrito_ventana.title("Carrito")
        carrito_ventana.geometry("400x300")

        total = 0
        for item, cantidad, subtotal in carrito:
            tk.Label(carrito_ventana, text=f"{cantidad} x {item}: $ {subtotal}").pack(anchor="w")
            total += subtotal

        tk.Label(carrito_ventana, text=f"\nTotal: $ {total}", font=("Arial", 14)).pack()

        tk.Button(carrito_ventana, text="Pagar", command=lambda: seleccionar_metodo_pago(total, carrito_ventana)).pack(pady=10)

    def seleccionar_metodo_pago(total, ventana):
        ventana.destroy()
        ventana_metodo = tk.Toplevel(ventana_principal)
        ventana_metodo.title("Método de Pago")
        ventana_metodo.geometry("300x200")

        tk.Label(ventana_metodo, text="Seleccione un método de pago:", font=("Arial", 14)).pack(pady=10)

        tk.Button(ventana_metodo, text="Efectivo", command=lambda: pagar_efectivo(total, ventana_metodo), bg="green", fg="white").pack(pady=5)
        tk.Button(ventana_metodo, text="Tarjeta", command=lambda: pagar_tarjeta(total, ventana_metodo), bg="blue", fg="white").pack(pady=5)

    def pagar_efectivo(total, ventana):
        messagebox.showinfo("Pago Exitoso", f"Gracias por su compra. Total pagado en efectivo: $ {total}")
        carrito.clear()
        ventana.destroy()

    def pagar_tarjeta(total, ventana):
        ventana.destroy()
        mostrar_pago_tarjeta(total)

    def mostrar_pago_tarjeta(total):
        ventana_pago = tk.Toplevel(ventana_principal)
        ventana_pago.title("Pago con Tarjeta")
        ventana_pago.geometry("400x400")

        tk.Label(ventana_pago, text="Información de Pago", font=("Arial", 16)).pack(pady=10)

        tk.Label(ventana_pago, text="Nombre del Titular:").pack(pady=5)
        entry_nombre = tk.Entry(ventana_pago)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_pago, text="Número de Tarjeta:").pack(pady=5)
        entry_tarjeta = tk.Entry(ventana_pago)
        entry_tarjeta.pack(pady=5)

        tk.Label(ventana_pago, text="Fecha de Caducidad (MM/AA):").pack(pady=5)
        entry_caducidad = tk.Entry(ventana_pago)
        entry_caducidad.pack(pady=5)

        tk.Label(ventana_pago, text="Código de Seguridad:").pack(pady=5)
        entry_cvv = tk.Entry(ventana_pago, show="*")
        entry_cvv.pack(pady=5)

        def procesar_pago():
            nombre = entry_nombre.get()
            tarjeta = entry_tarjeta.get()
            caducidad = entry_caducidad.get()
            cvv = entry_cvv.get()

            if not nombre or not tarjeta or not caducidad or not cvv:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")
                return

            if not tarjeta.isdigit() or len(tarjeta) != 16:
                messagebox.showerror("Error", "Número de tarjeta inválido.")
                return

            if not cvv.isdigit() or len(cvv) != 3:
                messagebox.showerror("Error", "Código de seguridad inválido.")
                return

            messagebox.showinfo("Pago Exitoso", f"Gracias por su compra. Total pagado: $ {total}")
            ventana_pago.destroy()

        tk.Button(ventana_pago, text="Pagar", command=procesar_pago, bg="green", fg="white").pack(pady=20)

    # Títulos
    titulo = tk.Label(ventana_principal, text="Menú de Comida Rápida", font=("Arial", 16))
    titulo.pack(pady=10)

    # Dibujos de Hamburguesas
    frame_burger = tk.Frame(ventana_principal)
    frame_burger.pack(pady=5)
    canvas_burger = tk.Canvas(frame_burger, width=100, height=100)
    canvas_burger.pack(side=tk.LEFT, padx=10)
    dibujar_comida(canvas_burger, "hamburguesa", 10, 10)
    tk.Label(frame_burger, text="Hamburguesa ($5):").pack(side=tk.LEFT, padx=5)
    tk.Entry(frame_burger, textvariable=cant_burger, width=5).pack(side=tk.LEFT)
    tk.Button(frame_burger, text="Agregar", command=lambda: agregar_al_carrito("Hamburguesa", cant_burger.get(), 5)).pack(side=tk.LEFT, padx=5)

    # Dibujos de Pizzas
    frame_pizza = tk.Frame(ventana_principal)
    frame_pizza.pack(pady=5)
    canvas_pizza = tk.Canvas(frame_pizza, width=100, height=100)
    canvas_pizza.pack(side=tk.LEFT, padx=10)
    dibujar_comida(canvas_pizza, "pizza", 50, 10)
    tk.Label(frame_pizza, text="Pizza ($8):").pack(side=tk.LEFT, padx=5)
    tk.Entry(frame_pizza, textvariable=cant_pizza, width=5).pack(side=tk.LEFT)
    tk.Button(frame_pizza, text="Agregar", command=lambda: agregar_al_carrito("Pizza", cant_pizza.get(), 8)).pack(side=tk.LEFT, padx=5)

    # Dibujos de Bebidas
    frame_bebida = tk.Frame(ventana_principal)
    frame_bebida.pack(pady=5)
    canvas_bebida = tk.Canvas(frame_bebida, width=100, height=100)
    canvas_bebida.pack(side=tk.LEFT, padx=10)
    dibujar_comida(canvas_bebida, "bebida", 30, 10)
    tk.Label(frame_bebida, text="Bebida ($2):").pack(side=tk.LEFT, padx=5)
    tk.Entry(frame_bebida, textvariable=cant_bebida, width=5).pack(side=tk.LEFT)
    tk.Button(frame_bebida, text="Agregar", command=lambda: agregar_al_carrito("Bebida", cant_bebida.get(), 2)).pack(side=tk.LEFT, padx=5)

    # Botones
    frame_botones = tk.Frame(ventana_principal)
    frame_botones.pack(pady=10)
    tk.Button(frame_botones, text="Ver Carrito", command=ver_carrito, bg="blue", fg="white").pack(side=tk.LEFT, padx=10)

    ventana_principal.mainloop()

# Ventana de Inicio de Sesión
ventana_login = tk.Tk()
ventana_login.title("Inicio de Sesión")
ventana_login.geometry("300x300")
ventana_login.configure(bg="lightblue")

# Widgets de inicio de sesión
frame_login = tk.Frame(ventana_login, bg="lightblue")
frame_login.pack(pady=20)

tk.Label(frame_login, text="Usuario:", bg="lightblue", font=("Arial", 12)).pack(pady=5)
entry_usuario_login = tk.Entry(frame_login)
entry_usuario_login.pack(pady=5)

tk.Label(frame_login, text="Contraseña:", bg="lightblue", font=("Arial", 12)).pack(pady=5)
entry_contrasena_login = tk.Entry(frame_login, show="*")
entry_contrasena_login.pack(pady=5)

frame_botones = tk.Frame(ventana_login, bg="lightblue")
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Iniciar Sesión", command=iniciar_sesion, bg="green", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(frame_botones, text="Registrar", command=mostrar_registro, bg="orange", fg="white").pack(side=tk.LEFT, padx=10)

ventana_login.mainloop()
