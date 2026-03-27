nombre = "alice"
conectado = True
contraseña = "1234"

if conectado == False:
    print(nombre, "ESTA ONLINE")
else:
    print(nombre, "Esta Desconectado")

# Validar contraseñas

password_correcta = "1234"
password_ingresada = "1234"

if password_ingresada == password_correcta:
    print("LOGIN EXITOSO, Bienvenido")
elif password_ingresada == "":
    print("NO INGRESO LA COTRASEÑA, ERROR")
else:
    print("ERROR:CONTRASEÑA INCORRECTA")
