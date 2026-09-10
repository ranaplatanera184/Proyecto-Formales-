import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Token import Token
from AnalisisSintactico import AnalisisSintactico
from gestor_reglas import GestorReglas
from almacenamiento import Almacenamiento


def test_revisarCorreo_valido():
    tokens = [
        Token("PALABRA RESERVADA", "CORREO"),
        Token("DOS PUNTOS", ":"),
        Token("PALABRA", "juan"),
        Token("PUNTO", "."),
        Token("PALABRA", "perez"),
        Token("NUMERO", "01"),
        Token("ARROBA", "@"),
        Token("PALABRA", "uptc"),
        Token("PUNTO", "."),
        Token("PALABRA", "edu"),
        Token("PUNTO", "."),
        Token("PALABRA", "co")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_revisarCorreo_invalido():
    tokens = [
        Token("PALABRA RESERVADA", "CORREO"),
        Token("DOS PUNTOS", ":"),
        Token("PALABRA", "invalido")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is False


def test_revisarContrasena_valida():
    tokens = [
        Token("PALABRA RESERVADA", "CONTRASEÑA"),
        Token("DOS PUNTOS", ":"),
        Token("LETRA", "M"),
        Token("LETRA", "i"),
        Token("LETRA", "C"),
        Token("LETRA", "l"),
        Token("LETRA", "a"),
        Token("LETRA", "v"),
        Token("LETRA", "e"),
        Token("NUMERO", "123"),
        Token("ESPECIAL", "!")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_revisarContrasena_debil():
    tokens = [
        Token("PALABRA RESERVADA", "CONTRASEÑA"),
        Token("DOS PUNTOS", ":"),
        Token("LETRA", "c"),
        Token("LETRA", "o"),
        Token("LETRA", "r"),
        Token("LETRA", "t"),
        Token("LETRA", "a")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is False


def test_revisarCerrar():
    tokens = [
        Token("PALABRA RESERVADA", "CERRAR")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is False


def test_token_inesperado():
    tokens = [
        Token("PALABRA", "invalido")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
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
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    try:
        analizador.revisarSintaxis()
        assert False, "Debería haber lanzado SyntaxError"
    except SyntaxError as e:
        assert "No hay token" in str(e)


def test_revisar_historial():
    tokens = [
        Token("PALABRA RESERVADA", "HISTORIAL")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_revisar_usuarios():
    tokens = [
        Token("PALABRA RESERVADA", "USUARIOS")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_revisar_ayuda():
    tokens = [
        Token("PALABRA RESERVADA", "AYUDA")
    ]
    gestor = GestorReglas()
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True


def test_revisar_exportar(tmp_path):
    tokens = [
        Token("PALABRA RESERVADA", "EXPORTAR")
    ]
    almac = Almacenamiento()
    almac.agregar_correo("test@uptc.edu.co")
    gestor = GestorReglas(almacenamiento=almac)
    analizador = AnalisisSintactico(tokens, gestorReglas=gestor)
    resultado = analizador.revisarSintaxis()
    assert resultado is True
    assert os.path.exists("exportacion.json")
    os.remove("exportacion.json")


def test_revisar_validar():
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
