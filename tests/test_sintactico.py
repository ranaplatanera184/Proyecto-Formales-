import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Token import Token
from AnalisisSintactico import AnalisisSintactico


def test_revisarCorreo_valido():
    tokens = [
        Token("PALABRA RESERVADA", "CORREO"),
        Token("DOS PUNTOS", ":"),
        Token("CORREO", "juan.perez@uptc.edu.co")
    ]
    analizador = AnalisisSintactico(tokens)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_revisarCorreo_invalido():
    tokens = [
        Token("PALABRA RESERVADA", "CORREO"),
        Token("DOS PUNTOS", ":"),
        Token("PALABRA", "invalido")
    ]
    analizador = AnalisisSintactico(tokens)
    resultado = analizador.revisarSintaxis()
    assert resultado is False


def test_revisarContrasena_valida():
    tokens = [
        Token("PALABRA RESERVADA", "CONTRASEÑA"),
        Token("DOS PUNTOS", ":"),
        Token("CADENA", "MiClave123!")
    ]
    analizador = AnalisisSintactico(tokens)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_revisarContrasena_debil():
    tokens = [
        Token("PALABRA RESERVADA", "CONTRASEÑA"),
        Token("DOS PUNTOS", ":"),
        Token("CADENA", "corta")
    ]
    analizador = AnalisisSintactico(tokens)
    resultado = analizador.revisarSintaxis()
    assert resultado is False


def test_revisarCerrar():
    tokens = [
        Token("PALABRA RESERVADA", "CERRAR")
    ]
    analizador = AnalisisSintactico(tokens)
    resultado = analizador.revisarSintaxis()
    assert resultado is False


def test_token_inesperado():
    tokens = [
        Token("PALABRA", "invalido")
    ]
    analizador = AnalisisSintactico(tokens)
    try:
        analizador.revisarSintaxis()
        assert False, "Debería haber lanzado SyntaxError"
    except SyntaxError as e:
        assert "Token inesperado" in str(e)


def test_falta_valor_correo():
    tokens = [
        Token("PALABRA RESERVADA", "CORREO"),
        Token("DOS PUNTOS", ":")
    ]
    analizador = AnalisisSintactico(tokens)
    try:
        analizador.revisarSintaxis()
        assert False, "Debería haber lanzado SyntaxError"
    except SyntaxError as e:
        assert "No hay token" in str(e)
