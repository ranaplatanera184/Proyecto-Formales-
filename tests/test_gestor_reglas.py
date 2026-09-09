import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Token import Token
from AnalisisSintactico import AnalisisSintactico
from gestor_reglas import GestorReglas
from almacenamiento import Almacenamiento


def test_obtener_regla():
    gestor = GestorReglas()
    regla = gestor.obtenerRegla("CORREO")
    assert regla is not None
    assert regla["nombreRegla"] == "ValidarCorreo"


def test_obtener_regla_no_existe():
    gestor = GestorReglas()
    regla = gestor.obtenerRegla("NOEXISTE")
    assert regla is None


def test_ejecutar_validar_correo_valido():
    tokens = [
        Token("PALABRA RESERVADA", "CORREO"),
        Token("DOS PUNTOS", ":"),
        Token("CORREO", "juan.perez@uptc.edu.co")
    ]
    almac = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True
    assert "juan.perez@uptc.edu.co" in almac.obtener_historial()


def test_ejecutar_validar_correo_invalido():
    tokens = [
        Token("PALABRA RESERVADA", "CORREO"),
        Token("DOS PUNTOS", ":"),
        Token("PALABRA", "invalido")
    ]
    almac = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True
    assert len(almac.obtener_historial()) == 0


def test_ejecutar_validar_contrasena_valida():
    tokens = [
        Token("PALABRA RESERVADA", "CONTRASEÑA"),
        Token("DOS PUNTOS", ":"),
        Token("CADENA", "MiClave123!")
    ]
    almac = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_ejecutar_validar_contrasena_debil():
    tokens = [
        Token("PALABRA RESERVADA", "CONTRASEÑA"),
        Token("DOS PUNTOS", ":"),
        Token("CADENA", "corta")
    ]
    almac = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_ejecutar_salir():
    tokens = [
        Token("PALABRA RESERVADA", "CERRAR")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is False


def test_ejecutar_mostrar_historial():
    tokens = [
        Token("PALABRA RESERVADA", "HISTORIAL")
    ]
    almac = Almacenamiento()
    almac.agregar_correo("test@uptc.edu.co")
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_ejecutar_mostrar_usuarios():
    tokens = [
        Token("PALABRA RESERVADA", "USUARIOS")
    ]
    almac = Almacenamiento()
    almac.agregar_usuario("test@uptc.edu.co", "Clave123!")
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_ejecutar_ayuda():
    tokens = [
        Token("PALABRA RESERVADA", "AYUDA")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_ejecutar_regla_no_existe():
    tokens = [
        Token("PALABRA RESERVADA", "NOEXISTE")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    try:
        analizador.revisarSintaxis()
        assert False, "Debería haber lanzado SyntaxError"
    except SyntaxError as e:
        assert "No existe una regla" in str(e)


def test_historial_acumula_correos():
    tokens1 = [
        Token("PALABRA RESERVADA", "CORREO"),
        Token("DOS PUNTOS", ":"),
        Token("CORREO", "juan.perez@uptc.edu.co")
    ]
    tokens2 = [
        Token("PALABRA RESERVADA", "CORREO"),
        Token("DOS PUNTOS", ":"),
        Token("CORREO", "ana.garcia@uptc.edu.co")
    ]
    almac = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almac)

    analizador1 = AnalisisSintactico(tokens1, gestorReglas=gestor)
    analizador1.revisarSintaxis()

    analizador2 = AnalisisSintactico(tokens2, gestorReglas=gestor)
    analizador2.revisarSintaxis()

    assert len(almac.obtener_historial()) == 2
    assert almac.obtener_historial()[0] == "juan.perez@uptc.edu.co"
    assert almac.obtener_historial()[1] == "ana.garcia@uptc.edu.co"


def test_obtener_regla_validar():
    gestor = GestorReglas()
    regla = gestor.obtenerRegla("VALIDAR")
    assert regla is not None
    assert regla["nombreRegla"] == "ValidarCredenciales"
    assert regla["tipo"] == "validar_interactivo"


def test_ejecutar_validar_interactivo_exitoso():
    tokens = [
        Token("PALABRA RESERVADA", "VALIDAR")
    ]
    almac = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)

    with patch('builtins.input', side_effect=["juan.perez@uptc.edu.co", "MiClave123!"]):
        resultado = analizador.revisarSintaxis()

    assert resultado is True
    assert "juan.perez@uptc.edu.co" in almac.obtener_historial()
    assert len(almac.obtener_usuarios()) == 1
    assert almac.obtener_usuarios()[0]["correo"] == "juan.perez@uptc.edu.co"
    assert almac.obtener_usuarios()[0]["contrasena"] == "MiClave123!"


def test_ejecutar_validar_interactivo_correo_invalido():
    tokens = [
        Token("PALABRA RESERVADA", "VALIDAR")
    ]
    almac = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)

    with patch('builtins.input', side_effect=["invalido"]):
        resultado = analizador.revisarSintaxis()

    assert resultado is True
    assert len(almac.obtener_historial()) == 0
    assert len(almac.obtener_usuarios()) == 0


def test_ejecutar_validar_interactivo_contrasena_debil():
    tokens = [
        Token("PALABRA RESERVADA", "VALIDAR")
    ]
    almac = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)

    with patch('builtins.input', side_effect=["juan.perez@uptc.edu.co", "corta"]):
        resultado = analizador.revisarSintaxis()

    assert resultado is True
    assert len(almac.obtener_historial()) == 0
    assert len(almac.obtener_usuarios()) == 0


def test_ejecutar_validar_interactivo_correo_guardado():
    tokens = [
        Token("PALABRA RESERVADA", "VALIDAR")
    ]
    almac = Almacenamiento()
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)

    with patch('builtins.input', side_effect=["ana.garcia@uptc.edu.co", "OtraClave456!"]):
        resultado = analizador.revisarSintaxis()

    assert resultado is True
    assert "ana.garcia@uptc.edu.co" in almac.obtener_historial()
    assert almac.obtener_usuarios()[0]["correo"] == "ana.garcia@uptc.edu.co"
    assert almac.obtener_usuarios()[0]["contrasena"] == "OtraClave456!"
