import socket
import threading

# Configuración
HOST = "127.0.0.1"  # IP local de tu propia PC
PORT = 5555          # puerto de conexión

clientes = []        # lista de clientes conectados

def manejar_cliente(conn, addr):
    print("Cliente conectado:", addr)
    while True:
        try:
            mensaje = conn.recv(1024).decode()
            if mensaje:
                print("Mensaje recibido:", mensaje)
                broadcast(mensaje, conn)
        except:
            clientes.remove(conn)
            conn.close()
            break

def broadcast(mensaje, remitente):
    for cliente in clientes:
        if cliente != remitente:
            try:
                cliente.send(mensaje.encode())
            except:
                clientes.remove(cliente)

# Iniciar servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print("Servidor iniciado en", HOST, ":", PORT)
print("Esperando conexiones...")

while True:
    conn, addr = servidor.accept()
    clientes.append(conn)
    hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
    hilo.start()