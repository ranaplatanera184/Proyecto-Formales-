from Token import Token
from gestor_reglas import GestorReglas
from validaciones import validacion_correo, validacion_contrasena


class AnalisisSintactico:

    def __init__(self, tokens, rutaReglas="reglas.json"):
        self.tokens = tokens
        self.pos = 0
        self.gestorReglas = GestorReglas(rutaReglas)
        self.errores = []

    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self, tipo):
        token = self.actual()
        if token is None:
            raise SyntaxError("No hay token")
        if token.token != tipo:
            raise SyntaxError(f"Se esperaba {tipo} y llegó {token.token} ({token.valor})")
        self.pos = self.pos + 1
        return token

    def consumir_o(self, tipos):
        token = self.actual()
        if token is None:
            raise SyntaxError("No hay token")
        if token.token not in tipos:
            raise SyntaxError(f"Se esperaba uno de {tipos} y llegó {token.token} ({token.valor})")
        self.pos = self.pos + 1
        return token

    def revisarSintaxis(self):
        while self.pos < len(self.tokens):
            token = self.actual()
            if token is None:
                break

            if token.token == "PALABRA RESERVADA":
                operacion = token.valor.upper()
                regla = self.gestorReglas.obtenerRegla(operacion)

                if regla is None:
                    raise SyntaxError(f"No existe una regla definida para '{operacion}'")

                metodo = getattr(self, regla["metodo"], None)
                if metodo is None:
                    raise SyntaxError(f"La regla '{regla['nombreRegla']}' apunta a un método inexistente")

                resultado = metodo()
                if resultado is not None:
                    return resultado
            else:
                raise SyntaxError(f"Token inesperado: {token.token} ({token.valor})")

        return True

    def revisarCorreo(self):
        self.consumir("PALABRA RESERVADA")
        self.consumir("DOS PUNTOS")
        token_valor = self.consumir_o(["CORREO", "PALABRA", "VALOR"])
        correo = token_valor.valor
        errores = validacion_correo(correo)
        if errores:
            print("ERRORES EN EL CORREO:")
            for error in errores:
                print("-", error)
            return False
        print("CORREO VALIDO:", correo)
        return True

    def revisarContrasena(self):
        self.consumir("PALABRA RESERVADA")
        self.consumir("DOS PUNTOS")
        token_contrasena = self.actual()
        if token_contrasena and token_contrasena.token in ["CADENA", "VALOR", "PALABRA"]:
            contrasena = token_contrasena.valor
            self.pos += 1
        else:
            raise SyntaxError("Se esperaba una contraseña (CADENA, VALOR o PALABRA)")

        errores = validacion_contrasena(contrasena)
        if errores:
            print("ERRORES EN LA CONTRASEÑA:")
            for error in errores:
                print("-", error)
            return False
        print("CONTRASEÑA VALIDA")
        return True

    def revisarCerrar(self):
        self.consumir("PALABRA RESERVADA")
        print("Ejecución detenida")
        return False
