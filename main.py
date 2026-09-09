from ImplementacionAnalisisLexico import tokenizar_correo_completo
from AnalisisSintactico import AnalisisSintactico
from gestor_reglas import GestorReglas
from almacenamiento import Almacenamiento

print("=== SISTEMA DE VALIDACION DE CREDENCIALES ===")
print("Comandos disponibles:")
print("  VALIDAR                  - Validar correo y contraseña")
print("  CORREO: ejemplo@dominio.com")
print("  CONTRASEÑA: \"MiContraseña123!\"")
print("  HISTORIAL")
print("  USUARIOS")
print("  EXPORTAR")
print("  AYUDA")
print("  CERRAR")
print("==============================================")

almacenamiento = Almacenamiento()
gestor = GestorReglas(almacenamiento=almacenamiento)

while True:
    texto = input("SISTEMA> ")

    tokens, errores = tokenizar_correo_completo(texto)

    print("\nTOKENS:")
    for token in tokens:
        print(token)

    if errores:
        print("\nERRORES LEXICOS:")
        for error in errores:
            print(error)
        continue

    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    try:
        resultado = analizador.revisarSintaxis()
        if resultado is False:
            break
    except SyntaxError as e:
        print(f"ERROR DE SINTAXIS: {e}")
