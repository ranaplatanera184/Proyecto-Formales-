from gestor_reglas import GestorReglas


class AnalisisSintactico:

    def __init__(self, tokens, gestorReglas=None, rutaReglas="reglas.json", almacenamiento=None):
        self.tokens = tokens
        self.pos = 0
        if gestorReglas:
            self.gestorReglas = gestorReglas
        else:
            self.gestorReglas = GestorReglas(rutaReglas, almacenamiento)
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
                resultado = self.gestorReglas.ejecutar(operacion, self)
                self.pos += 1
                if resultado is not None:
                    return resultado
            else:
                raise SyntaxError(f"Token inesperado: {token.token} ({token.valor})")

        return True
