import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Token import Token
from ImplementacionAnalisisLexico import tokenizar, tokenizar_correo_completo, tokenizar_contrasena_completo


def test_tokenizar_correo():
    tokens, errores = tokenizar('"juan.perez@uptc.edu.co"')
    assert len(tokens) == 1
    assert tokens[0].token == "CADENA"
    assert tokens[0].valor == "juan.perez@uptc.edu.co"
    assert len(errores) == 0


def test_tokenizar_contrasena():
    tokens, errores = tokenizar('"MiClave123!"')
    assert len(tokens) == 1
    assert tokens[0].token == "CADENA"
    assert tokens[0].valor == "MiClave123!"
    assert len(errores) == 0


def test_tokenizar_cerrar():
    tokens, errores = tokenizar("CERRAR")
    assert len(tokens) == 1
    assert tokens[0].token == "PALABRA RESERVADA"
    assert tokens[0].valor == "CERRAR"
    assert len(errores) == 0


def test_tokenizar_error_caracter():
    tokens, errores = tokenizar("correo ~")
    assert len(errores) > 0
    assert "ERROR LEXICO" in errores[0]


def test_tokenizar_cadena_sin_cerrar():
    tokens, errores = tokenizar('"cadena sin cerrar')
    assert len(errores) > 0
    assert "sin cerrar" in errores[0]


def test_tokenizar_completo():
    tokens, errores = tokenizar('CORREO: "juan.perez@uptc.edu.co"')
    assert len(tokens) == 3
    assert tokens[0].token == "PALABRA RESERVADA"
    assert tokens[1].token == "DOS PUNTOS"
    assert tokens[2].token == "CADENA"
    assert len(errores) == 0


def test_tokenizar_correo_completo():
    tokens, errores = tokenizar_correo_completo('CORREO: "juan.perez@uptc.edu.co"')
    assert len(tokens) == 3
    assert tokens[0].token == "PALABRA RESERVADA"
    assert tokens[1].token == "DOS PUNTOS"
    assert tokens[2].token == "CORREO"
    assert tokens[2].valor == "juan.perez@uptc.edu.co"
    assert len(errores) == 0


def test_tokenizar_correo_con_numeros():
    tokens, errores = tokenizar_correo_completo('CORREO: "juan.perez01@uptc.edu.co"')
    assert len(tokens) == 3
    assert tokens[2].token == "CORREO"
    assert tokens[2].valor == "juan.perez01@uptc.edu.co"
    assert len(errores) == 0


def test_tokenizar_punto():
    tokens, errores = tokenizar(".")
    assert len(tokens) == 1
    assert tokens[0].token == "PUNTO"
    assert tokens[0].valor == "."
    assert len(errores) == 0


def test_tokenizar_arroba():
    tokens, errores = tokenizar("@")
    assert len(tokens) == 1
    assert tokens[0].token == "ARROBA"
    assert tokens[0].valor == "@"
    assert len(errores) == 0


def test_tokenizar_numero():
    tokens, errores = tokenizar("123")
    assert len(tokens) == 1
    assert tokens[0].token == "NUMERO"
    assert tokens[0].valor == "123"
    assert len(errores) == 0


def test_tokenizar_contrasena_completo():
    tokens = tokenizar_contrasena_completo("MiClave123!")
    assert len(tokens) == 9
    assert tokens[0].token == "LETRA"
    assert tokens[0].valor == "M"
    assert tokens[7].token == "NUMERO"
    assert tokens[7].valor == "123"
    assert tokens[8].token == "ESPECIAL"
    assert tokens[8].valor == "!"


def test_tokenizar_contrasena_solo_letras():
    tokens = tokenizar_contrasena_completo("abcdef")
    assert len(tokens) == 6
    for token in tokens:
        assert token.token == "LETRA"


def test_tokenizar_contrasena_solo_numeros():
    tokens = tokenizar_contrasena_completo("12345")
    assert len(tokens) == 1
    assert tokens[0].token == "NUMERO"
    assert tokens[0].valor == "12345"


def test_tokenizar_contrasena_solo_especiales():
    tokens = tokenizar_contrasena_completo("!@#")
    assert len(tokens) == 3
    for token in tokens:
        assert token.token == "ESPECIAL"


def test_tokenizar_contrasena_vacia():
    tokens = tokenizar_contrasena_completo("")
    assert len(tokens) == 0
