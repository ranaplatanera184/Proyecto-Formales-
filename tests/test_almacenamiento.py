import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from almacenamiento import Almacenamiento


def test_agregar_correo():
    almac = Almacenamiento()
    almac.agregar_correo("juan.perez@uptc.edu.co")
    assert almac.obtener_historial() == ["juan.perez@uptc.edu.co"]


def test_agregar_multiples_correos():
    almac = Almacenamiento()
    almac.agregar_correo("juan.perez@uptc.edu.co")
    almac.agregar_correo("ana.garcia@uptc.edu.co")
    assert len(almac.obtener_historial()) == 2


def test_historial_vacio():
    almac = Almacenamiento()
    assert almac.obtener_historial() == []


def test_agregar_usuario():
    almac = Almacenamiento()
    almac.agregar_usuario("juan.perez@uptc.edu.co", "MiClave123!")
    usuarios = almac.obtener_usuarios()
    assert len(usuarios) == 1
    assert usuarios[0]["correo"] == "juan.perez@uptc.edu.co"
    assert usuarios[0]["contrasena"] == "MiClave123!"


def test_agregar_multiples_usuarios():
    almac = Almacenamiento()
    almac.agregar_usuario("juan.perez@uptc.edu.co", "Clave123!")
    almac.agregar_usuario("ana.garcia@uptc.edu.co", "OtraClave456!")
    assert len(almac.obtener_usuarios()) == 2


def test_usuarios_vacios():
    almac = Almacenamiento()
    assert almac.obtener_usuarios() == []


def test_exportar_json(tmp_path):
    almac = Almacenamiento()
    almac.agregar_correo("test@uptc.edu.co")
    almac.agregar_usuario("test@uptc.edu.co", "Clave123!")

    ruta = str(tmp_path / "test_export.json")
    resultado = almac.exportar_json(ruta)
    assert resultado == ruta
    assert os.path.exists(ruta)

    import json
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
    assert datos["historial_correos"] == ["test@uptc.edu.co"]
    assert len(datos["usuarios"]) == 1


def test_exportar_json_default():
    almac = Almacenamiento()
    almac.agregar_correo("test@uptc.edu.co")
    ruta = almac.exportar_json()
    assert os.path.exists(ruta)
    os.remove(ruta)
