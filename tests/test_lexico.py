import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ImplementacionAnalisisLexico import tokenizar, tokenizar_correo_completo


def test_tokenizar_correo():
    tokens, errores = tokenizar_correo_completo("CORREO: juan.perez@uptc.edu.co")
    assert len(errores) == 0
    assert len(tokens) == 3
    assert tokens[0].token == "PALABRA RESERVADA"
    assert tokens[0].valor == "CORREO"
    assert tokens[1].token == "DOS PUNTOS"
    assert tokens[2].token == "CORREO"
    assert tokens[2].valor == "juan.perez@uptc.edu.co"


def test_tokenizar_contrasena():
    tokens, errores = tokenizar('CONTRASEÑA: "MiClave123!"')
    assert len(errores) == 0
    assert len(tokens) == 3
    assert tokens[0].token == "PALABRA RESERVADA"
    assert tokens[0].valor == "CONTRASEÑA"
    assert tokens[1].token == "DOS PUNTOS"
    assert tokens[2].token == "CADENA"
    assert tokens[2].valor == "MiClave123!"


def test_tokenizar_cerrar():
    tokens, errores = tokenizar("CERRAR")
    assert len(errores) == 0
    assert len(tokens) == 1
    assert tokens[0].token == "PALABRA RESERVADA"
    assert tokens[0].valor == "CERRAR"


def test_tokenizar_error_caracter():
    tokens, errores = tokenizar("CORREO: juan.perez@uptc.edu.co $")
    assert len(errores) > 0
    assert "ERROR LEXICO" in errores[0]


def test_tokenizar_cadena_sin_cerrar():
    tokens, errores = tokenizar('CONTRASEÑA: "sin_cerrar')
    assert len(errores) > 0
    assert "Cadena sin cerrar" in errores[0]


def test_tokenizar_completo():
    tokens, errores = tokenizar_correo_completo("CORREO: juan.perez@uptc.edu.co, CONTRASEÑA: \"Clave456!\"")
    assert len(errores) == 0
    assert len(tokens) >= 6


def test_tokenizar_correo_completo():
    tokens, errores = tokenizar_correo_completo("CORREO: juan.perez@uptc.edu.co")
    assert len(errores) == 0
    assert len(tokens) == 3
    assert tokens[2].token == "CORREO"
    assert tokens[2].valor == "juan.perez@uptc.edu.co"


def test_tokenizar_correo_con_numeros():
    tokens, errores = tokenizar_correo_completo("CORREO: juan.perez01@uptc.edu.co")
    assert len(errores) == 0
    assert len(tokens) == 3
    assert tokens[2].token == "CORREO"
    assert tokens[2].valor == "juan.perez01@uptc.edu.co"
