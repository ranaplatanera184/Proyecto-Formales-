class Token:

    def __init__(self, token, valor):
        self.token = token
        self.valor = valor

    def to_json(self):
        return {
            "token": self.token,
            "valor": self.valor,
        }

    def __repr__(self):
        return f"Token(token={self.token}, valor={self.valor!r})"
    
    
#hacer un analisis lexico para cada uno de los tokens que vaya encontrando