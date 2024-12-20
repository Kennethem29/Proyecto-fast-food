import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def cargar_imagen(ruta, size):
    try:
        return ImageTk.PhotoImage(Image.open(ruta).resize(size))
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró la imagen: {ruta}")
        return None

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
    ventana_registro.geometry("300x200")

    tk.Label(ventana_registro, text="Usuario:").pack(pady=5)
    entry_usuario = tk.Entry(ventana_registro)
    entry_usuario.pack(pady=5)

    tk.Label(ventana_registro, text="Contraseña:").pack(pady=5)
    entry_contrasena = tk.Entry(ventana_registro, show="*")
    entry_contrasena.pack(pady=5)

    tk.Button(ventana_registro, text="Registrar", command=registrar_usuario).pack(pady=10)

def mostrar_menu_principal():
    # Ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Pedido de Comida Rápida")
    ventana_principal.geometry("500x500")
    ventana_principal.resizable(False, False)

    # Variables
    cant_burger = tk.StringVar(value="0")
    cant_pizza = tk.StringVar(value="0")
    cant_bebida = tk.StringVar(value="0")
    resultado = tk.StringVar(value="Total: $ 0")

    def calcular_total():
        try:
            total = (int(cant_burger.get()) * 5) + \
                    (int(cant_pizza.get()) * 8) + \
                    (int(cant_bebida.get()) * 2)
            resultado.set(f"Total: $ {total}")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos en las cantidades.")

    def limpiar():
        cant_burger.set("0")
        cant_pizza.set("0")
        cant_bebida.set("0")
        resultado.set("Total: $ 0")

    # Títulos
    titulo = tk.Label(ventana_principal, text="Menú de Comida Rápida", font=("Arial", 16))
    titulo.pack(pady=10)

    # Cargar imágenes
    img_burger = cargar_imagen("hamburguesa.jpg", (100, 100))
    img_pizza = cargar_imagen("pizza.jpg", (100, 100))
    img_bebida = cargar_imagen("bebida.jpg", (100, 100))

    # Sección de Hamburguesas
    frame_burger = tk.Frame(ventana_principal)
    frame_burger.pack(pady=5)
    if img_burger:
        img_label_burger = tk.Label(frame_burger, image=img_burger)
        img_label_burger.pack(side=tk.LEFT, padx=10)
    tk.Label(frame_burger, text="Hamburguesa ($5):").pack(side=tk.LEFT, padx=5)
    tk.Entry(frame_burger, textvariable=cant_burger, width=5).pack(side=tk.LEFT)

    # Sección de Pizzas
    frame_pizza = tk.Frame(ventana_principal)
    frame_pizza.pack(pady=5)
    if img_pizza:
        img_label_pizza = tk.Label(frame_pizza, image=img_pizza)
        img_label_pizza.pack(side=tk.LEFT, padx=10)
    tk.Label(frame_pizza, text="Pizza ($8):").pack(side=tk.LEFT, padx=5)
    tk.Entry(frame_pizza, textvariable=cant_pizza, width=5).pack(side=tk.LEFT)

    # Sección de Bebidas
    frame_bebida = tk.Frame(ventana_principal)
    frame_bebida.pack(pady=5)
    if img_bebida:
        img_label_bebida = tk.Label(frame_bebida, image=img_bebida)
        img_label_bebida.pack(side=tk.LEFT, padx=10)
    tk.Label(frame_bebida, text="Bebida ($2):").pack(side=tk.LEFT, padx=5)
    tk.Entry(frame_bebida, textvariable=cant_bebida, width=5).pack(side=tk.LEFT)

    # Botones
    frame_botones = tk.Frame(ventana_principal)
    frame_botones.pack(pady=10)
    tk.Button(frame_botones, text="Calcular Total", command=calcular_total, bg="green", fg="white").pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="Limpiar", command=limpiar, bg="red", fg="white").pack(side=tk.LEFT, padx=10)

    # Resultado
    label_resultado = tk.Label(ventana_principal, textvariable=resultado, font=("Arial", 14))
    label_resultado.pack(pady=20)

    ventana_principal.mainloop()

# Ventana de Inicio de Sesión
ventana_login = tk.Tk()
ventana_login.title("Inicio de Sesión")
ventana_login.geometry("300x250")

# Widgets de inicio de sesión
tk.Label(ventana_login, text="Usuario:").pack(pady=5)
entry_usuario_login = tk.Entry(ventana_login)
entry_usuario_login.pack(pady=5)

tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
entry_contrasena_login = tk.Entry(ventana_login, show="*")
entry_contrasena_login.pack(pady=5)

tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
tk.Button(ventana_login, text="Registrar", command=mostrar_registro).pack(pady=10)

ventana_login.mainloop()
