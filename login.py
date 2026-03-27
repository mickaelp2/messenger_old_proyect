import json

# ---- FUNCIONES ----

def registrar_usuario(nombre, email, password):
    with open("usuarios.json", "r") as archivo:
        datos = json.load(archivo)
    
    for usuario in datos:
        if usuario["email"] == email:
            print("Error: ese email ya está registrado")
            return
    
    nuevo = {"nombre": nombre, "email": email, 
             "password": password, "estado": "Online"}
    datos.append(nuevo)
    
    with open("usuarios.json", "w") as archivo:
        json.dump(datos, archivo)
    
    print("Usuario registrado:", nombre)


def verificar_login(email, password):
    with open("usuarios.json", "r") as archivo:
        datos = json.load(archivo)
    
    for usuario in datos:
        if usuario["email"] == email:
            if usuario["password"] == password:
                print("Login exitoso, bienvenido", usuario["nombre"])
                return
            else:
                print("Error: contraseña incorrecta")
                return
    
    print("Error: ese email no está registrado")


# ---- PROGRAMA ----

print("=== MSN Messenger ===")
print("1. Registrar usuario")
print("2. Iniciar sesión")

opcion = input("Elige una opción: ")

if opcion == "1":
    nombre   = input("Nombre: ")
    email    = input("Email: ")
    password = input("Contraseña: ")
    registrar_usuario(nombre, email, password)

elif opcion == "2":
    email    = input("Email: ")
    password = input("Contraseña: ")
    verificar_login(email, password)

else:
    print("Opción no válida")