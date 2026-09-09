import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validaciones import validacion_correo, validacion_contrasena, validar_credenciales


def test_correo_valido():
    errores = validacion_correo("juan.perez@uptc.edu.co")
    assert len(errores) == 0


def test_correo_con_numeros():
    errores = validacion_correo("juan.perez01@uptc.edu.co")
    assert len(errores) == 0


def test_correo_un_digito():
    errores = validacion_correo("juan.perez9@uptc.edu.co")
    assert len(errores) == 0


def test_correo_dos_digitos():
    errores = validacion_correo("juan.perez99@uptc.edu.co")
    assert len(errores) == 0


def test_correo_vacio():
    errores = validacion_correo("")
    assert len(errores) > 0
    assert "vacio" in errores[0].lower()


def test_correo_otro_dominio():
    errores = validacion_correo("juan.perez@gmail.com")
    assert len(errores) > 0
    assert "formato valido" in errores[0].lower()


def test_correo_sin_punto():
    errores = validacion_correo("juanperez@uptc.edu.co")
    assert len(errores) > 0


def test_correo_tres_digitos():
    errores = validacion_correo("juan.perez123@uptc.edu.co")
    assert len(errores) > 0


def test_correo_formato_invalido():
    errores = validacion_correo("test@")
    assert len(errores) > 0


def test_contrasena_valida():
    errores = validacion_contrasena("MiClave123!")
    assert len(errores) == 0


def test_contrasena_corta():
    errores = validacion_contrasena("Ab1!")
    assert len(errores) > 0
    assert "8 caracteres" in errores[0]


def test_contrasena_sin_mayuscula():
    errores = validacion_contrasena("miclave123!")
    assert len(errores) > 0
    assert "mayuscula" in errores[0].lower()


def test_contrasena_sin_minuscula():
    errores = validacion_contrasena("MICLAVE123!")
    assert len(errores) > 0
    assert "minuscula" in errores[0].lower()


def test_contrasena_sin_numero():
    errores = validacion_contrasena("MiClave!")
    assert len(errores) > 0
    assert "numero" in errores[0].lower()


def test_contrasena_sin_especial():
    errores = validacion_contrasena("MiClave123")
    assert len(errores) > 0
    assert "especial" in errores[0].lower()


def test_contrasena_con_espacios():
    errores = validacion_contrasena("Mi Clave 123!")
    assert len(errores) > 0
    assert "espacios" in errores[0].lower()


def test_validar_credenciales_validas():
    resultado = validar_credenciales("juan.perez@uptc.edu.co", "MiClave123!")
    assert resultado is True


def test_validar_credenciales_invalidas():
    resultado = validar_credenciales("invalido", "corta")
    assert resultado is False
