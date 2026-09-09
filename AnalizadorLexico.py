from Token import Token
import re


def Tokenizar(cadena):

    tokens = []
    errores = []

    i = 0
    n = len(cadena)

    palabrasReservadas = {
        "CORREO",
        "CONTRASEÑA"
    }

    simbolos = {
        "," : "COMA",
        ":" : "DOS PUNTOS",
        ";" : "PUNTO Y COMA"
    }

    patron_correo = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    patron_identificador = r"^[a-zA-Z0-9._%+-]+$"


    while i < n:

        cdn = cadena[i]


        if cdn.isspace():

            i += 1
            continue


        if cdn == '"':

            inicio = i
            i += 1

            while i < n and cadena[i] != '"':
                i += 1

            if i >= n:

                errores.append(f"ERROR LEXICO: Cadena sin cerrar en la posicion {inicio}")
                break

            i += 1
            valor = cadena[inicio + 1:i - 1]
            tokens.append(Token("CADENA", valor))
            continue


        if cdn.isalpha():

            inicio = i

            while i < n and (cadena[i].isalpha() or cadena[i] in "ñÑ"):
                i += 1

            palabra = cadena[inicio:i]

            if palabra.upper() in palabrasReservadas:
                tokens.append(Token("PALABRA RESERVADA", palabra.upper()))

            else:
                tokens.append(Token("PALABRA", palabra))

            continue


        if cdn.isalnum() or cdn in "._%-+@#":

            inicio = i

            while i < n and (cadena[i].isalnum() or cadena[i] in "._%+-@#!$%^&*()?:;{}|<>"):
                i += 1

            valor = cadena[inicio:i]

            if re.fullmatch(patron_correo, valor):

                tokens.append(Token("CORREO", valor))
                continue

            else:

                tokens.append(Token("VALOR", valor))
                continue


        if cdn in simbolos:

            tokens.append(Token(simbolos[cdn], cdn))
            i += 1
            continue

        errores.append(f"ERROR LEXICO: Caracter no reconocido '{cdn}'")
        i += 1

    return tokens, errores


def validacion_correo(correo):

    errores = []

    patron_correo = (
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )


    if correo == "":
        errores.append("El correo no puede estar vacio")
        return errores


    if not re.fullmatch(patron_correo, correo):
        errores.append("El correo no tiene un formato valido")


    if "@" not in correo:
        errores.append("El correo debe contener @")


    if correo.startswith("@"):
        errores.append("El correo no puede comenzar con @")


    if correo.endswith("@"):
        errores.append("El correo no puede terminar con @")


    if ".." in correo:
        errores.append("El correo no puede contener dos puntos consecutivos")


    return errores


def validacion_contraseña(contraseña):

    errores = []


    if len(contraseña) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres")


    if not re.search(r"[A-Z]", contraseña):

        errores.append("La contraseña debe contener al menos una letra mayuscula")


    if not re.search(r"[a-z]", contraseña):
        errores.append("La contraseña debe contener al menos una letra minuscula")


    if not re.search(r"[0-9]", contraseña):

        errores.append("La contraseña debe contener al menos un numero")


    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contraseña):
        errores.append("La contraseña debe contener al menos un caracter especial")


    if re.search(r"\s", contraseña):
        errores.append("La contraseña no puede contener espacios en blanco")


    return errores


def validar_credenciales(correo, contraseña):

    errores_correo = validacion_correo(correo)
    errores_contraseña = validacion_contraseña(contraseña)


    if errores_correo:

        print("ERRORES EN EL CORREO:")
        for error in errores_correo:
            print("-", error)


    if errores_contraseña:

        print("ERRORES EN LA CONTRASEÑA:")
        for error in errores_contraseña:
            print("-", error)


    if not errores_correo and not errores_contraseña:

        print("CREDENCIALES VALIDAS")
        return True


    print("CREDENCIALES INVALIDAS")
    return False


cadena = input("Ponga sus credenciales: ")

tokens, errores = Tokenizar(cadena)

print("\nTOKENS:")
for token in tokens:
    print(token)


if errores:

    print("ERRORES LEXICOS:")
    for error in errores:
        print(error)

else:

    correo = ""
    contraseña = ""


    for token in tokens:

        if token.token == "CORREO":
            correo = token.valor


        if token.token == "VALOR":
            contraseña = token.valor


        if token.token == "CADENA":
            contraseña = token.valor


    validar_credenciales(correo, contraseña)