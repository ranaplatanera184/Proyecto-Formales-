import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ImplementacionAnalisisLexico import tokenizar, tokenizar_correo_completo


def test_tokenizar_correo():
    tokens, errores = tokenizar("CORREO: juan.perez@uptc.edu.co")
    assert len(errores) == 0
    assert len(tokens) == 11
    assert tokens[0].token == "PALABRA RESERVADA"
    assert tokens[0].valor == "CORREO"
    assert tokens[1].token == "DOS PUNTOS"
    assert tokens[2].token == "PALABRA"
    assert tokens[2].valor == "juan"
    assert tokens[3].token == "PUNTO"
    assert tokens[3].valor == "."
    assert tokens[4].token == "PALABRA"
    assert tokens[4].valor == "perez"
    assert tokens[5].token == "ARROBA"
    assert tokens[5].valor == "@"
    assert tokens[6].token == "PALABRA"
    assert tokens[6].valor == "uptc"
    assert tokens[7].token == "PUNTO"
    assert tokens[8].token == "PALABRA"
    assert tokens[8].valor == "edu"
    assert tokens[9].token == "PUNTO"
    assert tokens[10].token == "PALABRA"
    assert tokens[10].valor == "co"


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
    tokens, errores = tokenizar("CORREO: juan.perez@uptc.edu.co, CONTRASEÑA: \"Clave456!\"")
    assert len(errores) == 0
    assert len(tokens) >= 15


def test_tokenizar_correo_completo():
    tokens, errores = tokenizar_correo_completo("CORREO: juan.perez@uptc.edu.co")
    assert len(errores) == 0
    assert len(tokens) == 11
    assert tokens[2].token == "PALABRA"
    assert tokens[2].valor == "juan"
    assert tokens[3].token == "PUNTO"
    assert tokens[4].token == "PALABRA"
    assert tokens[4].valor == "perez"
    assert tokens[5].token == "ARROBA"


def test_tokenizar_correo_con_numeros():
    tokens, errores = tokenizar_correo_completo("CORREO: juan.perez01@uptc.edu.co")
    assert len(errores) == 0
    assert len(tokens) == 12
    assert tokens[5].token == "NUMERO"
    assert tokens[5].valor == "01"
    assert tokens[6].token == "ARROBA"


def test_tokenizar_punto():
    tokens, errores = tokenizar("CORREO: juan.perez@uptc.edu.co")
    assert len(errores) == 0
    assert any(t.token == "PUNTO" and t.valor == "." for t in tokens)


def test_tokenizar_arroba():
    tokens, errores = tokenizar("CORREO: juan.perez@uptc.edu.co")
    assert len(errores) == 0
    assert any(t.token == "ARROBA" and t.valor == "@" for t in tokens)


def test_tokenizar_numero():
    tokens, errores = tokenizar("CORREO: juan.perez01@uptc.edu.co")
    assert len(errores) == 0
    assert any(t.token == "NUMERO" and t.valor == "01" for t in tokens)
