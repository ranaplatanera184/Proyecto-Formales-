import sys
import os

from ImplementacionAnalisisLexico import tokenizar_correo_completo, tokenizar_linea_completo
from AnalisisSintactico import AnalisisSintactico
from gestor_reglas import GestorReglas
from almacenamiento import Almacenamiento

EXTENSION = ".jace"


def ejecutar_linea(texto, gestor, almacenamiento):
    texto = texto.strip()

    if not texto:
        return None

    if texto.startswith("#"):
        return None

    tokens, errores = tokenizar_linea_completo(texto)

    if errores:
        print("\nERRORES LEXICOS:")
        for error in errores:
            print(error)
        return False

    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    try:
        resultado = analizador.revisarSintaxis()
        return resultado
    except SyntaxError as e:
        print(f"ERROR DE SINTAXIS: {e}")
        return False


def ejecutar_archivo(ruta, almacenamiento):
    if not os.path.exists(ruta):
        print(f"Error: el archivo '{ruta}' no existe")
        return False

    if not ruta.lower().endswith(EXTENSION):
        print(f"Error: el archivo debe tener la extensión {EXTENSION}")
        return False

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except Exception as error:
        print(f"Error leyendo el archivo: {error}")
        return False

    if not lineas or all(linea.strip() == "" for linea in lineas):
        print("El archivo está vacío")
        return False

    print(f"\n=== Ejecutando {ruta} ===\n")

    gestor = GestorReglas(almacenamiento=almacenamiento)

    for i, linea in enumerate(lineas, 1):
        linea_limpia = linea.strip()

        if not linea_limpia or linea_limpia.startswith("#"):
            continue

        print(f"Línea {i}: {linea_limpia}")

        resultado = ejecutar_linea(linea_limpia, gestor, almacenamiento)

        if resultado is False:
            print(f"\nEjecución detenida en línea {i}")
            return False

    print("\n=== Archivo ejecutado exitosamente ===")
    return True


def modo_interactivo():
    print("\n=== SISTEMA DE VALIDACION DE CREDENCIALES (.jace) ===")
    print("Comandos disponibles:")
    print("  VALIDAR                  - Validar correo y contraseña")
    print("  CORREO: ejemplo@uptc.edu.co")
    print("  CONTRASEÑA: \"MiContraseña123!\"")
    print("  HISTORIAL")
    print("  USUARIOS")
    print("  EXPORTAR")
    print("  AYUDA")
    print("  CERRAR")
    print("=====================================================")

    almacenamiento = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almacenamiento)

    while True:
        try:
            texto = input("\nJACE> ")
        except KeyboardInterrupt:
            print("\nPrograma terminado")
            break
        except EOFError:
            print("\nPrograma terminado")
            break

        resultado = ejecutar_linea(texto, gestor, almacenamiento)

        if resultado is False:
            break


def mostrar_ayuda():
    print("\nJACE Language - FACULTAD SECCIONAL SOGAMOSO")
    print("\nUso:")
    print("  python main.py                    - Modo interactivo")
    print(f"  python main.py archivo{EXTENSION}  - Ejecutar archivo")
    print(f"  python main.py --help             - Mostrar esta ayuda")
    print(f"\nExtensión soportada: {EXTENSION}")
    print("\nFormato del archivo:")
    print("  - Una instrucción por línea")
    print("  - Líneas que empiecen con # son ignoradas (comentarios)")
    print("  - Líneas vacías son ignoradas")
    print("\nEjemplo de archivo .jace:")
    print('  CORREO: juan.perez@uptc.edu.co')
    print('  CONTRASEÑA: "MiClave123!"')
    print("  HISTORIAL")
    print("  CERRAR")


def main():
    if len(sys.argv) == 1:
        modo_interactivo()
        return

    if sys.argv[1] in ["--help", "-h"]:
        mostrar_ayuda()
        return

    if len(sys.argv) == 2:
        ruta = sys.argv[1]
        almacenamiento = Almacenamiento()
        ejecutar_archivo(ruta, almacenamiento)
        return

    print("Error: cantidad de argumentos inválida")
    mostrar_ayuda()


if __name__ == "__main__":
    main()
