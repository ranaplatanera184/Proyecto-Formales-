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
        "," : "COMA",
        ":" : "DOS PUNTOS",
        ";" : "PUNTO Y COMA"
    }

    patron_correo = r"^[a-zA-Z]+\.[a-zA-Z]+[0-9]{0,2}@uptc\.edu\.co$"

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


def tokenizar_correo_completo(cadena):
    tokens, errores = tokenizar(cadena)

    tokens_corregidos = []
    i = 0
    while i < len(tokens):
        if (tokens[i].token == "PALABRA" and
            i + 1 < len(tokens) and
            tokens[i + 1].token == "VALOR" and
            (tokens[i + 1].valor.startswith("@") or tokens[i + 1].valor.startswith("."))):

            correo_completo = tokens[i].valor + tokens[i + 1].valor
            tokens_corregidos.append(Token("CORREO", correo_completo))
            i += 2
        else:
            tokens_corregidos.append(tokens[i])
            i += 1

    return tokens_corregidos, errores
