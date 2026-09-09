from ImplementacionAnalisisLexico import tokenizar_correo_completo
from AnalisisSintactico import AnalisisSintactico

print("=== SISTEMA DE VALIDACION DE CREDENCIALES ===")
print("Comandos disponibles:")
print("  CORREO: ejemplo@dominio.com")
print("  CONTRASEÑA: \"MiContraseña123!\"")
print("  CERRAR")
print("==============================================")

while True:
    texto = input("CREDENCIALES> ")

    tokens, errores = tokenizar_correo_completo(texto)

    print("\nTOKENS:")
    for token in tokens:
        print(token)

    if errores:
        print("\nERRORES LEXICOS:")
        for error in errores:
            print(error)
        continue

    analizador = AnalisisSintactico(tokens)
    try:
        resultado = analizador.revisarSintaxis()
        if not resultado:
            break
    except SyntaxError as e:
        print(f"ERROR DE SINTAXIS: {e}")
