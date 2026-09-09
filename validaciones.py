import re


def validacion_correo(correo):
    errores = []

    patron_correo = r"^[a-zA-Z]+\.[a-zA-Z]+[0-9]{0,2}@uptc\.edu\.co$"

    if correo == "":
        errores.append("El correo no puede estar vacio")
        return errores

    if not re.fullmatch(patron_correo, correo):
        errores.append("El correo no tiene un formato valido (use: nombre.apellido@uptc.edu.co)")

    return errores


def validacion_contrasena(contrasena):
    errores = []

    if len(contrasena) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres")

    if not re.search(r"[A-Z]", contrasena):
        errores.append("La contraseña debe contener al menos una letra mayuscula")

    if not re.search(r"[a-z]", contrasena):
        errores.append("La contraseña debe contener al menos una letra minuscula")

    if not re.search(r"[0-9]", contrasena):
        errores.append("La contraseña debe contener al menos un numero")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
        errores.append("La contraseña debe contener al menos un caracter especial")

    if re.search(r"\s", contrasena):
        errores.append("La contraseña no puede contener espacios en blanco")

    return errores


def validar_credenciales(correo, contrasena):
    errores_correo = validacion_correo(correo)
    errores_contrasena = validacion_contrasena(contrasena)

    if errores_correo:
        print("ERRORES EN EL CORREO:")
        for error in errores_correo:
            print("-", error)

    if errores_contrasena:
        print("ERRORES EN LA CONTRASEÑA:")
        for error in errores_contrasena:
            print("-", error)

    if not errores_correo and not errores_contrasena:
        print("CREDENCIALES VALIDAS")
        return True

    print("CREDENCIALES INVALIDAS")
    return False
