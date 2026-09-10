from Token import Token
import re


def tokenizar(cadena):
    tokens = []
    errores = []

    i = 0
    n = len(cadena)

    palabrasReservadas = {
        "CORREO",
        "CONTRASEÑA",
        "CERRAR",
        "HISTORIAL",
        "USUARIOS",
        "EXPORTAR",
        "AYUDA",
        "VALIDAR"
    }

    simbolos = {
        ",": "COMA",
        ":": "DOS PUNTOS",
        ";": "PUNTO Y COMA",
        ".": "PUNTO",
        "@": "ARROBA"
    }

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

        if cdn.isdigit():
            inicio = i

            while i < n and cadena[i].isdigit():
                i += 1

            numero = cadena[inicio:i]
            tokens.append(Token("NUMERO", numero))
            continue

        if cdn in simbolos:
            tokens.append(Token(simbolos[cdn], cdn))
            i += 1
            continue

        errores.append(f"ERROR LEXICO: Caracter no reconocido '{cdn}'")
        i += 1

    return tokens, errores


def tokenizar_correo_completo(cadena):
    tokens, errores = tokenizar(cadena)

    tokens_corregidos = []
    for token in tokens:
        if token.token == "CADENA":
            tokens_corregidos.append(Token("CORREO", token.valor))
        else:
            tokens_corregidos.append(token)

    return tokens_corregidos, errores


def tokenizar_contrasena_completo(cadena):
    tokens = []
    i = 0
    n = len(cadena)

    caracteres_especiales = "!@#$%^&*(),.?\":{}|<>"

    while i < n:
        char = cadena[i]

        if char.isalpha():
            tokens.append(Token("LETRA", char))
            i += 1
        elif char.isdigit():
            inicio = i
            while i < n and cadena[i].isdigit():
                i += 1
            tokens.append(Token("NUMERO", cadena[inicio:i]))
        elif char in caracteres_especiales:
            tokens.append(Token("ESPECIAL", char))
            i += 1
        else:
            tokens.append(Token("ESPECIAL", char))
            i += 1

    return tokens


def tokenizar_linea_completo(cadena):
    tokens, errores = tokenizar(cadena)

    tokens_corregidos = []
    for token in tokens:
        if token.token == "CADENA" and any(t.token == "PALABRA RESERVADA" and t.valor == "CONTRASEÑA" for t in tokens_corregidos):
            tokens_contrasena = tokenizar_contrasena_completo(token.valor)
            tokens_corregidos.extend(tokens_contrasena)
        elif token.token == "CADENA":
            tokens_corregidos.append(Token("CORREO", token.valor))
        else:
            tokens_corregidos.append(token)

    return tokens_corregidos, errores
