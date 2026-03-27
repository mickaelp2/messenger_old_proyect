import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

nombre = input("Tu nombre: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

print("Conectado al servidor. Escribe tus mensajes:")

def recibir():
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            print(mensaje)
        except:
            break

hilo = threading.Thread(target=recibir)
hilo.daemon = True
hilo.start()

while True:
    mensaje = input("")
    cliente.send((nombre + ": " + mensaje).encode())