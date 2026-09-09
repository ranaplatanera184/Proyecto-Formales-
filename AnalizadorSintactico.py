from Token import Token

def _init_(self, tokens):
    self.tokens = []
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

def revisarSintaxis(self):
    self.pos = 0
    while self.pos < len(self.tokens):
        token = self.actual()
        if token.token == "CORREO":
            self.consumir("CORREO")
            self.consumir("DOS_PUNTOS")
            self.consumir("PALABRA")
            self.consumir("ARROBA")
            self.consumir("PALABRA")
            
        elif token.token == "CONTRASEÑA":
            self.consumir("CONTRASEÑA")
            self.consumir("DOS_PUNTOS")
            self.consumir("CADENA")
        else:
            raise SyntaxError(f"Token inesperado: {token.token} ({token.valor})")