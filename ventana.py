import tkinter as tk
import json
import socket
import threading
import winsound
import os

ventana = tk.Tk()
ventana.title("MSN Messenger")
ventana.geometry("300x400")
ventana.configure(bg="#0078D7")

label = tk.Label(ventana, text="MSN Messenger",
                 bg="#0078D7", fg="white",
                 font=("Arial", 18, "bold"))
label.pack(pady=30)

label_email = tk.Label(ventana, text="Correo electrónico:",
                       bg="#0078D7", fg="white")
label_email.pack()

entry_email = tk.Entry(ventana, width=30)
entry_email.pack(pady=5)

label_pass = tk.Label(ventana, text="Contraseña:",
                      bg="#0078D7", fg="white")
label_pass.pack()

entry_pass = tk.Entry(ventana, width=30, show="*")
entry_pass.pack(pady=5)

boton = tk.Button(ventana, text="Entrar", width=20)
boton.pack(pady=20)


def abrir_chat(usuario, contacto):
    chat = tk.Toplevel()
    chat.title("Chat con " + contacto["nombre"])
    chat.geometry("350x450")
    chat.configure(bg="white")

    tk.Label(chat,
             text="Conversación con " + contacto["nombre"],
             bg="#0078D7", fg="white",
             font=("Arial", 11, "bold")).pack(fill="x", pady=5)

    area = tk.Text(chat, height=18, width=40,
    
                   state="disabled", bg="#f5f5f5",
                   font=("Arial", 10))
    area.pack(pady=5, padx=10)
     # Cargar historial anterior
    nombre_archivo = "chat_" + usuario["nombre"] + "_" + contacto["nombre"] + ".txt"
    
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as f:
            historial = f.read()
        area.config(state="normal")
        area.insert("end", historial)
        area.see("end")
        area.config(state="disabled")

    # Indicador "Escribiendo..." — aparece debajo del área de mensajes
    label_escribiendo = tk.Label(chat, text="",
                                  bg="white", fg="gray",
                                  font=("Arial", 9, "italic"))
    label_escribiendo.pack()

    frame = tk.Frame(chat, bg="white")
    frame.pack(fill="x", padx=10, pady=5)

    entry_msg = tk.Entry(frame, width=30, font=("Arial", 10))
    entry_msg.pack(side="left", padx=5)

    # Conectar al servidor
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("127.0.0.1", 5555))
        cliente.send(usuario["nombre"].encode())
    except:
        area.config(state="normal")
        area.insert("end", "⚠ No se pudo conectar al servidor\n")
        area.config(state="disabled")
        return

    # Recibir mensajes en hilo separado
    def recibir():
        while True:
            try:
                mensaje = cliente.recv(1024).decode()
                if mensaje.startswith("ESCRIBIENDO:"):
                    # Es una notificación de que alguien está escribiendo
                    nombre_digitando = mensaje.split(":")[1]
                    label_escribiendo.config(text=nombre_digitando + " está escribiendo...")
                    # Borra el indicador después de 2 segundos
                    chat.after(2000, lambda: label_escribiendo.config(text=""))
                else:
                    # Es un mensaje normal
                    label_escribiendo.config(text="")
                     # Sonido al recibir mensaje ← línea nueva
                    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                    area.config(state="normal")
                    area.insert("end", mensaje + "\n")
                    area.see("end")
                    area.config(state="disabled")
                   # Guardar en historial — solo mensajes reales
                    if not mensaje.startswith("ESCRIBIENDO:"):
                        with open(nombre_archivo, "a") as f:
                            f.write(mensaje + "\n")
            except:
                break

    hilo = threading.Thread(target=recibir)
    hilo.daemon = True
    hilo.start()

    # Detectar cuando el usuario está escribiendo
    def esta_escribiendo(event):
        try:
            cliente.send(("ESCRIBIENDO:" + usuario["nombre"]).encode())
        except:
            pass

    entry_msg.bind("<KeyPress>", esta_escribiendo)

    def enviar():
        mensaje = entry_msg.get()
        if mensaje != "":
            try:
                cliente.send((usuario["nombre"] + ": " + mensaje).encode())
                area.config(state="normal")
                area.insert("end", "Tú: " + mensaje + "\n")
                area.see("end")
                area.config(state="disabled")
                entry_msg.delete(0, "end")
                # Guardar en historial ← línea nueva
                with open(nombre_archivo, "a") as f:
                    f.write("Tú: " + mensaje + "\n")
            except:
                area.config(state="normal")
                area.insert("end", "⚠ Error al enviar\n")
                area.config(state="disabled")

    tk.Button(frame, text="Enviar", command=enviar,
              bg="#0078D7", fg="white").pack(side="left")

    entry_msg.bind("<Return>", lambda e: enviar())


def abrir_contactos(usuario):
    contactos = tk.Tk()
    contactos.title("MSN Messenger — Contactos")
    contactos.geometry("250x500")
    contactos.configure(bg="#0078D7")

    tk.Label(contactos,
             text=usuario["nombre"],
             bg="#0078D7", fg="white",
             font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(contactos,
             text=usuario["estado"],
             bg="#0078D7", fg="white",
             font=("Arial", 10)).pack()

    tk.Label(contactos, text="─── Contactos ───",
             bg="#0078D7", fg="white").pack(pady=10)

    with open("usuarios.json", "r") as archivo:
        todos = json.load(archivo)

    for contacto in todos:
        if contacto["email"] != usuario["email"]:
            btn = tk.Button(contactos,
                            text="● " + contacto["nombre"] + " — " + contacto["estado"],
                            bg="#0078D7", fg="white",
                            font=("Arial", 11),
                            border=0,
                            cursor="hand2",
                            command=lambda c=contacto: abrir_chat(usuario, c))
            btn.pack(pady=3)

    contactos.mainloop()


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
                label_resultado.config(text="Contraseña incorrecta", fg="red")
                return

    label_resultado.config(text="Email no registrado", fg="red")


boton.config(command=iniciar_sesion)

label_resultado = tk.Label(ventana, text="", bg="#0078D7")
label_resultado.pack()

ventana.mainloop()