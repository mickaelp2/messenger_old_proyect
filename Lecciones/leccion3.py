# Función con return — devuelve un resultado
def verificar_login(email, password):
    email_correcto = "alice@msn.com"
    password_correcta = "1234"

    if email == email_correcto and password == password_correcta:
        return "LOGIN_OK"
    elif email != email_correcto:
        return "EMAIL_INCORRECTO"
    else:
        return "PASSWORD_INCORRECTA"

# Probando la función
resultado = verificar_login("alice@msn.com", "1234")
print(resultado)

resultado2 = verificar_login("bob@msn.com", "1234")
print(resultado2)

resultado3 = verificar_login("alice@msn.com", "9999")
print(resultado3)