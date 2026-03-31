import customtkinter as ctk
import tkinter as tk
from plyer import notification
import pygame
pygame.mixer.init()
from PIL import Image
import json
import socket
import threading
import winsound
import os

# Configuración visual global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ========================
# VENTANA DE LOGIN
# ========================
ventana = ctk.CTk()
ventana.title("MSN Messenger")
ventana.geometry("350x500")
ventana.resizable(False, False)

# Logo
try:
    logo_img = ctk.CTkImage(Image.open("MNS LOGO.png"), size=(100, 100))
    logo_label = ctk.CTkLabel(ventana, image=logo_img, text="")
    logo_label.pack(pady=20)
except:
    pass

# Título
ctk.CTkLabel(ventana, text="MSN Messenger",
             font=ctk.CTkFont(size=22, weight="bold")).pack(pady=5)

ctk.CTkLabel(ventana, text="Inicia sesión con tu cuenta",
             font=ctk.CTkFont(size=12),
             text_color="gray").pack(pady=2)

# Campos
entry_email = ctk.CTkEntry(ventana, width=280,
                            placeholder_text="Correo electrónico",
                            height=40, corner_radius=10)
entry_email.pack(pady=10)

entry_pass = ctk.CTkEntry(ventana, width=280,
                           placeholder_text="Contraseña",
                           show="*", height=40, corner_radius=10)
entry_pass.pack(pady=5)

# Label resultado
label_resultado = ctk.CTkLabel(ventana, text="", text_color="red",
                                font=ctk.CTkFont(size=11))
label_resultado.pack(pady=2)


def iniciar_sesion():
    email = entry_email.get()
    password = entry_pass.get()

    with open("usuarios.json", "r") as archivo:
        datos = json.load(archivo)

    for usuario in datos:
        if usuario["email"] == email:
            if usuario["password"] == password:
                ventana.destroy()
                abrir_contactos(usuario)
                return
            else:
                label_resultado.configure(text="Contraseña incorrecta")
                return

    label_resultado.configure(text="Email no registrado")


def abrir_registro():
    registro = ctk.CTkToplevel(ventana)
    registro.title("Crear cuenta")
    registro.geometry("350x450")
    registro.resizable(False, False)

    ctk.CTkLabel(registro, text="Crear cuenta",
                 font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

    entry_nombre = ctk.CTkEntry(registro, width=280,
                                 placeholder_text="Nombre",
                                 height=40, corner_radius=10)
    entry_nombre.pack(pady=8)

    entry_email_r = ctk.CTkEntry(registro, width=280,
                                  placeholder_text="Correo electrónico",
                                  height=40, corner_radius=10)
    entry_email_r.pack(pady=8)

    entry_pass_r = ctk.CTkEntry(registro, width=280,
                                 placeholder_text="Contraseña",
                                 show="*", height=40, corner_radius=10)
    entry_pass_r.pack(pady=8)

    entry_pass_r2 = ctk.CTkEntry(registro, width=280,
                                  placeholder_text="Confirmar contraseña",
                                  show="*", height=40, corner_radius=10)
    entry_pass_r2.pack(pady=8)

    label_res = ctk.CTkLabel(registro, text="", text_color="red")
    label_res.pack(pady=2)

    def crear_cuenta():
        nombre = entry_nombre.get()
        email = entry_email_r.get()
        password = entry_pass_r.get()
        password2 = entry_pass_r2.get()

        if nombre == "" or email == "" or password == "":
            label_res.configure(text="Completa todos los campos")
            return

        if password != password2:
            label_res.configure(text="Las contraseñas no coinciden")
            return

        with open("usuarios.json", "r") as archivo:
            datos = json.load(archivo)

        for usuario in datos:
            if usuario["email"] == email:
                label_res.configure(text="Ese email ya está registrado")
                return

        nuevo = {"nombre": nombre, "email": email,
                 "password": password, "estado": "Online"}
        datos.append(nuevo)

        with open("usuarios.json", "w") as archivo:
            json.dump(datos, archivo)

        label_res.configure(text="¡Cuenta creada!", text_color="green")
        registro.after(1500, registro.destroy)

    ctk.CTkButton(registro, text="Crear cuenta", width=280, height=40,
                  corner_radius=10, command=crear_cuenta).pack(pady=10)


# Botones
ctk.CTkButton(ventana, text="Iniciar sesión", width=280, height=40,
              corner_radius=10, command=iniciar_sesion).pack(pady=10)

ctk.CTkButton(ventana, text="Crear cuenta", width=280, height=40,
              corner_radius=10, fg_color="transparent",
              border_width=1, command=abrir_registro).pack(pady=2)

def elegir_avatar(usuario, callback):
    win = ctk.CTkToplevel()
    win.title("Elige tu avatar")
    win.geometry("350x400")
    win.resizable(False, False)
    win.grab_set()      # bloquea las otras ventanas
    win.focus_force()   # fuerza el foco en esta ventana

    ctk.CTkLabel(win, text="Elige tu avatar",
                 font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

    grid = ctk.CTkFrame(win)
    grid.pack(padx=20, pady=5)

    def seleccionar(path):
        with open("usuarios.json", "r") as f:
            datos = json.load(f)
        for u in datos:
            if u["email"] == usuario["email"]:
                u["avatar"] = path
                break
        with open("usuarios.json", "w") as f:
            json.dump(datos, f)
        usuario["avatar"] = path
        callback(path)
        win.destroy()

    def redondear_avatar(path, size):
        img = Image.open(path).resize((size, size))
        mascara = Image.new("L", (size, size), 0)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, size, size), fill=255)
        img_redonda = Image.new("RGBA", (size, size))
        img_redonda.paste(img, mask=mascara)
        return ctk.CTkImage(img_redonda, size=(size, size))

    for i in range(9):
        path = f"avatares/avatar-{i+1}.png"
        try:
            img = redondear_avatar(path, 80)
            btn = ctk.CTkButton(grid, image=img, text="",
                                width=80, height=80,
                                fg_color="transparent",
                                hover_color=("gray80", "gray30"),
                                command=lambda p=path: seleccionar(p))
            btn.grid(row=i//3, column=i%3, padx=8, pady=8)
        except:
            pass

    win.mainloop()

# ========================
# VENTANA DE CONTACTOS
# ========================
def abrir_contactos(usuario):
    contactos_win = ctk.CTk()
    contactos_win.title("MSN Messenger")
    contactos_win.geometry("280x550")
    contactos_win.minsize(280, 400)

   # Encabezado
    header = ctk.CTkFrame(contactos_win, corner_radius=0, height=90)
    header.pack(fill="x")
    header.pack_propagate(False)

    # Avatar a la izquierda
    avatar_path = usuario.get("avatar", "avatares/avatar-1.png")

    def redondear_imagen(path, size):
        img = Image.open(path).resize((size, size))
        mascara = Image.new("L", (size, size), 0)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, size, size), fill=255)
        img_redonda = Image.new("RGBA", (size, size))
        img_redonda.paste(img, mask=mascara)
        return ctk.CTkImage(img_redonda, size=(size, size))

    try:
        avatar_img = redondear_imagen(avatar_path, 60)
    except:
        avatar_img = None

    avatar_label = ctk.CTkLabel(header, image=avatar_img,
                                 text="", width=60, height=60)
    avatar_label.pack(side="left", padx=10, pady=15)

    # Info en el centro
    info = ctk.CTkFrame(header, fg_color="transparent")
    info.pack(side="left", fill="y", pady=10, expand=True)

    ctk.CTkLabel(info, text=usuario["nombre"],
                 font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w")

    estado_var = ctk.StringVar(value=usuario["estado"])
    estado_menu = ctk.CTkOptionMenu(info,
                                     values=["Online", "Ocupado", "Ausente", "Desconectado"],
                                     variable=estado_var, width=150)
    estado_menu.pack(anchor="w", pady=3)

    # Botón ⚙ a la derecha
    def actualizar_avatar(path):
        try:
            nueva_img = redondear_imagen(path, 60)
            avatar_label.configure(image=nueva_img)
        except:
            pass

    ctk.CTkButton(header, text="⚙", width=35, height=35,
                  corner_radius=8,
                  command=lambda: elegir_avatar(usuario, actualizar_avatar)).pack(side="right", padx=10)

def abrir_contactos(usuario):
    contactos_win = ctk.CTk()
    contactos_win.title("MSN Messenger")
    contactos_win.geometry("280x550")
    contactos_win.minsize(280, 400)

    # Encabezado
    header = ctk.CTkFrame(contactos_win, corner_radius=0, height=90)
    header.pack(fill="x")
    header.pack_propagate(False)

    avatar_path = usuario.get("avatar", "avatares/avatar-1.png")

    def redondear_imagen(path, size):
        img = Image.open(path).resize((size, size))
        mascara = Image.new("L", (size, size), 0)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, size, size), fill=255)
        img_redonda = Image.new("RGBA", (size, size))
        img_redonda.paste(img, mask=mascara)
        return ctk.CTkImage(img_redonda, size=(size, size))

    try:
        avatar_img = redondear_imagen(avatar_path, 60)
    except:
        avatar_img = None

    avatar_label = ctk.CTkLabel(header, image=avatar_img,
                                 text="", width=60, height=60)
    avatar_label.pack(side="left", padx=10, pady=15)

    info = ctk.CTkFrame(header, fg_color="transparent")
    info.pack(side="left", fill="y", pady=10, expand=True)

    ctk.CTkLabel(info, text=usuario["nombre"],
                 font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w")

    estado_var = ctk.StringVar(value=usuario["estado"])
    estado_menu = ctk.CTkOptionMenu(info,
                                     values=["Online", "Ocupado", "Ausente", "Desconectado"],
                                     variable=estado_var, width=150)
    estado_menu.pack(anchor="w", pady=3)

    def actualizar_avatar(path):
        try:
            nueva_img = redondear_imagen(path, 60)
            avatar_label.configure(image=nueva_img)
        except:
            pass

    ctk.CTkButton(header, text="⚙", width=35, height=35,
                  corner_radius=8,
                  command=lambda: elegir_avatar(usuario, actualizar_avatar)).pack(side="right", padx=10)

    # Botón agregar contacto
    def abrir_agregar_contacto():
        win = ctk.CTkToplevel(contactos_win)
        win.title("Agregar contacto")
        win.geometry("300x200")
        win.resizable(False, False)
        win.grab_set()
        win.focus_force()

        ctk.CTkLabel(win, text="Agregar contacto",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        entry_email_c = ctk.CTkEntry(win, width=250,
                                      placeholder_text="Email del contacto",
                                      height=38, corner_radius=10)
        entry_email_c.pack(pady=8)

        label_res = ctk.CTkLabel(win, text="", text_color="red")
        label_res.pack()

        def agregar():
            email_nuevo = entry_email_c.get()

            with open("usuarios.json", "r") as f:
                datos = json.load(f)

            existe = False
            for u in datos:
                if u["email"] == email_nuevo:
                    existe = True
                    break

            if not existe:
                label_res.configure(text="Usuario no encontrado")
                return

            if email_nuevo == usuario["email"]:
                label_res.configure(text="No puedes agregarte a ti mismo")
                return

            for u in datos:
                if u["email"] == usuario["email"]:
                    if email_nuevo in u["contactos"]:
                        label_res.configure(text="Ya es tu contacto")
                        return
                    u["contactos"].append(email_nuevo)
                    break

            with open("usuarios.json", "w") as f:
                json.dump(datos, f)

            label_res.configure(text="¡Contacto agregado!", text_color="green")
            win.after(1500, lambda: [win.destroy(), actualizar_contactos()])

        ctk.CTkButton(win, text="Agregar", width=250, height=38,
                      corner_radius=10, command=agregar).pack(pady=10)

    ctk.CTkButton(contactos_win, text="+ Agregar contacto",
                  width=200, height=35, corner_radius=10,
                  command=abrir_agregar_contacto).pack(pady=5)

    # Lista de contactos
    ctk.CTkLabel(contactos_win, text="── Contactos ──",
                 text_color="gray",
                 font=ctk.CTkFont(size=11)).pack(pady=5)

    scroll = ctk.CTkScrollableFrame(contactos_win)
    scroll.pack(fill="both", expand=True, padx=10, pady=5)

    def actualizar_contactos():
        for widget in scroll.winfo_children():
            widget.destroy()

        with open("usuarios.json", "r") as archivo:
            todos = json.load(archivo)

        mis_contactos = []
        for u in todos:
            if u["email"] == usuario["email"]:
                mis_contactos = u.get("contactos", [])
                break

        for contacto in todos:
            if contacto["email"] in mis_contactos:
                frame_contacto = ctk.CTkFrame(scroll, fg_color="transparent")
                frame_contacto.pack(fill="x", pady=3)

                avatar_path_c = contacto.get("avatar", "avatares/avatar-1.png")
                try:
                    avatar_c = redondear_imagen(avatar_path_c, 35)
                    ctk.CTkLabel(frame_contacto, image=avatar_c,
                                 text="", width=35, height=35).pack(side="left", padx=5)
                except:
                    pass

                colores = {
                    "Online":       "#00cc44",
                    "Ocupado":      "#ff3333",
                    "Ausente":      "#ffaa00",
                    "Desconectado": "#888888"
                }
                color = colores.get(contacto["estado"], "#888888")
                ctk.CTkLabel(frame_contacto, text="●",
                             text_color=color,
                             font=ctk.CTkFont(size=12),
                             width=15).pack(side="left")

                btn = ctk.CTkButton(frame_contacto,
                                    text=contacto["nombre"],
                                    anchor="w",
                                    fg_color="transparent",
                                    hover_color=("gray85", "gray25"),
                                    text_color=("black", "white"),
                                    command=lambda c=contacto: abrir_chat(usuario, c))
                btn.pack(side="left", fill="x", expand=True)

    actualizar_contactos()
    contactos_win.mainloop()


# ========================
# VENTANA DE CHAT
# ========================
def abrir_chat(usuario, contacto):
    chat = ctk.CTkToplevel()
    chat.title("Chat con " + contacto["nombre"])
    chat.geometry("400x500")
    chat.minsize(350, 400)

    # Encabezado chat
    header = ctk.CTkFrame(chat, corner_radius=0, height=55)
    header.pack(fill="x")
    header.pack_propagate(False)

    # Avatar del contacto
    avatar_contacto = contacto.get("avatar", "avatares/avatar-1.png")
    try:
        from PIL import ImageDraw
        img = Image.open(avatar_contacto).resize((40, 40))
        mascara = Image.new("L", (40, 40), 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, 40, 40), fill=255)
        img_redonda = Image.new("RGBA", (40, 40))
        img_redonda.paste(img, mask=mascara)
        avatar_chat = ctk.CTkImage(img_redonda, size=(40, 40))
        ctk.CTkLabel(header, image=avatar_chat, text="",
                     width=40, height=40).pack(side="left", padx=10, pady=7)
    except:
        pass

    ctk.CTkLabel(header,
                 text=contacto["nombre"],
                 font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", pady=7)

    # Área de mensajes
    area = ctk.CTkTextbox(chat, state="disabled",
                           font=ctk.CTkFont(size=12))
    area.pack(fill="both", expand=True, padx=10, pady=10)

    # Indicador escribiendo
    label_escribiendo = ctk.CTkLabel(chat, text="",
                                      text_color="gray",
                                      font=ctk.CTkFont(size=10, slant="italic"))
    label_escribiendo.pack(pady=2)

    # Frame inferior
    frame = ctk.CTkFrame(chat, corner_radius=0, height=55)
    frame.pack(fill="x")
    frame.pack_propagate(False)

    entry_msg = ctk.CTkEntry(frame, placeholder_text="Escribe un mensaje...",
                              height=38, corner_radius=10)
    entry_msg.pack(side="left", fill="x", expand=True, padx=10, pady=8)

    # Panel de emojis
    emojis = ["😊", "😂", "😢", "😡", "😎",
              "❤️", "👍", "🎉", "🔥", "💯",
              "😴", "🤔", "😅", "🥳", "👋",
              "😘", "🤣", "😭", "😤", "🤩"]

    def abrir_emojis():
        panel = ctk.CTkToplevel(chat)
        panel.title("")
        panel.geometry("250x200")
        panel.resizable(False, False)
        panel.attributes("-topmost", True)
        panel.grab_set()
        panel.focus_force()

        grid_emojis = ctk.CTkFrame(panel)
        grid_emojis.pack(fill="both", expand=True, padx=10, pady=10)

        def insertar_emoji(emoji):
            entry_msg.insert("end", emoji)
            panel.destroy()
            entry_msg.focus_set()

        for i, emoji in enumerate(emojis):
            btn = ctk.CTkButton(grid_emojis,
                                text=emoji,
                                width=40, height=40,
                                font=ctk.CTkFont(size=18),
                                fg_color="transparent",
                                hover_color=("gray80", "gray30"),
                                command=lambda e=emoji: insertar_emoji(e))
            btn.grid(row=i//5, column=i%5, padx=3, pady=3)

    # Botón emoji
    ctk.CTkButton(frame, text="😊", width=40, height=38,
                  corner_radius=10,
                  font=ctk.CTkFont(size=18),
                  fg_color="transparent",
                  hover_color=("gray80", "gray30"),
                  command=abrir_emojis).pack(side="left", padx=2, pady=8)

    # Conectar al servidor
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("127.0.0.1", 5555))
        cliente.send(usuario["nombre"].encode())
    except:
        area.configure(state="normal")
        area.insert("end", "⚠ No se pudo conectar al servidor\n")
        area.configure(state="disabled")
        return

    # Cargar historial
    nombre_archivo = "Historial/chat_" + usuario["nombre"] + "_" + contacto["nombre"] + ".txt"
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as f:
            historial = f.read()
        area.configure(state="normal")
        area.insert("end", historial)
        area.see("end")
        area.configure(state="disabled")

    def recibir():
        while True:
            try:
                mensaje = cliente.recv(1024).decode()
                if mensaje.startswith("ESCRIBIENDO:"):
                    nombre_digitando = mensaje.split(":")[1]
                    label_escribiendo.configure(text=nombre_digitando + " está escribiendo...")
                    chat.after(2000, lambda: label_escribiendo.configure(text=""))
                else:
                    label_escribiendo.configure(text="")
                    try:
                        notification.notify(
                            title="MSN Messenger — " + contacto["nombre"],
                            message=mensaje,
                            app_name="MSN Messenger",
                            timeout=4
                        )
                    except:
                        pass
                    try:
                        pygame.mixer.music.load("notificacion.mp3")
                        pygame.mixer.music.play()
                    except:
                        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                    area.configure(state="normal")
                    area.insert("end", mensaje + "\n")
                    area.see("end")
                    area.configure(state="disabled")
                    with open(nombre_archivo, "a") as f:
                        f.write(mensaje + "\n")
            except:
                break

    hilo = threading.Thread(target=recibir)
    hilo.daemon = True
    hilo.start()

    def esta_escribiendo(event):
        if event.keysym != "Return":
            try:
                cliente.send(("ESCRIBIENDO:" + usuario["nombre"]).encode())
            except:
                pass

    def enviar():
        mensaje = entry_msg.get()
        if mensaje != "":
            try:
                cliente.send((usuario["nombre"] + ": " + mensaje).encode("utf-8"))
                area.configure(state="normal")
                area.insert("end", "Tú: " + mensaje + "\n")
                area.see("end")
                area.configure(state="disabled")
                entry_msg.delete(0, "end")
                with open(nombre_archivo, "a") as f:
                    f.write("Tú: " + mensaje + "\n")
            except:
                area.configure(state="normal")
                area.insert("end", "⚠ Error al enviar\n")
                area.configure(state="disabled")

    ctk.CTkButton(frame, text="Enviar", width=80, height=38,
                  corner_radius=10, command=enviar).pack(side="left", padx=5, pady=8)

    entry_msg.bind("<KeyPress>", esta_escribiendo)
    entry_msg.bind("<Return>", lambda e: enviar())
ventana.mainloop()


