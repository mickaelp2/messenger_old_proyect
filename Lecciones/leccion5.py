# Lección 5 — Archivos JSON
import json

# Lista de usuarios
usuarios = [
    {"nombre": "Alice", "email": "alice@msn.com", "password": "1234", "estado": "Online"},
    {"nombre": "Bob",   "email": "bob@msn.com",   "password": "5678", "estado": "Ocupado"},
]

# Guardar en archivo
with open("usuarios.json", "w") as archivo:
    json.dump(usuarios, archivo)

print("Usuarios guardados correctamente")

# Leer el archivo que acabamos de crear
with open("usuarios.json", "r") as archivo:
    datos = json.load(archivo)

print("Usuarios cargados:")
for usuario in datos:
    print("-", usuario["nombre"], "→", usuario["estado"])

# Agregar un usuario nuevo sin borrar los anteriores
nuevo_usuario = {"nombre": "Carlos", "email": "carlos@msn.com", 
                 "password": "abcd", "estado": "Ausente"}

datos.append(nuevo_usuario)

with open("usuarios.json", "w") as archivo:
    json.dump(datos, archivo)

print("Carlos agregado correctamente")

# Verificar que quedaron los 3
with open("usuarios.json", "r") as archivo:
    verificar = json.load(archivo)

for usuario in verificar:
    print("-", usuario["nombre"])




def buscar_usuario(email):
    with open("usuarios.json", "r") as archivo:   
        datos = json.load(archivo)                
    for usuario in datos:                         
        if usuario["email"] == email:             
            print("Usuario encontrado:", usuario["nombre"]) 
            return
        print("USUARIO NO ENCONTRADO")


buscar_usuario("alice@msn.com")
buscar_usuario("pepe@msn.com")