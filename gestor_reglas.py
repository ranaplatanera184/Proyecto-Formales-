import json

class GestorReglas:
    def __init__(self, ruta="reglas.json"):
        with open(ruta, "r", encoding="utf-8") as archivo:
            self.reglas = json.load(archivo)

    def obtenerRegla(self, operacion):
        for regla in self.reglas:   
            if operacion in regla["palabras"]:
                return regla
        return None
