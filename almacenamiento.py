import json
import os


class Almacenamiento:
    def __init__(self):
        self.historial_correos = []
        self.usuarios = []

    def agregar_correo(self, correo):
        self.historial_correos.append(correo)

    def agregar_usuario(self, correo, contrasena):
        self.usuarios.append({"correo": correo, "contrasena": contrasena})

    def obtener_historial(self):
        return self.historial_correos

    def obtener_usuarios(self):
        return self.usuarios

    def exportar_json(self, ruta="exportacion.json"):
        datos = {
            "historial_correos": self.historial_correos,
            "usuarios": self.usuarios
        }
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
        return ruta
