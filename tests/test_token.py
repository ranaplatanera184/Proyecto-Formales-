import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Token import Token


def test_token_creation():
    token = Token("CORREO", "test@example.com")
    assert token.token == "CORREO"
    assert token.valor == "test@example.com"


def test_token_to_json():
    token = Token("PALABRA", "hola")
    json_data = token.to_json()
    assert json_data == {"token": "PALABRA", "valor": "hola"}


def test_token_repr():
    token = Token("CADENA", "secreto")
    repr_str = repr(token)
    assert "CADENA" in repr_str
    assert "secreto" in repr_str
