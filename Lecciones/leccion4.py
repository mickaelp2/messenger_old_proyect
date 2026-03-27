# Lección 4 — Listas

usuarios = ["Alice", "Bob", "Carlos", "Diana"]

print("Usuarios conectados:")

for usuario in usuarios:
    print("-", usuario)

# Diccionarios — varios datos por usuario
usuario1 = {
    "nombre": "Alice",
    "email": "alice@msn.com",
    "password": "1234",
    "estado": "Online"
}

print("---")
print("Nombre:", usuario1["nombre"])
print("Email:", usuario1["email"])
print("Estado:", usuario1["estado"])

# Lista de diccionarios — así se verá tu base de usuarios
usuarios = [
    {"nombre": "Alice", "email": "alice@msn.com", "estado": "Online"},
    {"nombre": "Bob",   "email": "bob@msn.com",   "estado": "Ocupado"},
    {"nombre": "Carlos","email": "carlos@msn.com", "estado": "Ausente"},
    {"nombre": "Diana","email": "diana@msn.com", "estado": "online"},
]

print("--- Lista de contactos ---")
for usuario in usuarios:
    print(usuario["nombre"], "→", usuario["estado"])