import json
from validaciones import validacion_correo, validacion_contrasena
from ImplementacionAnalisisLexico import tokenizar_correo_completo


class GestorReglas:
    def __init__(self, ruta="reglas.json", almacenamiento=None):
        with open(ruta, "r", encoding="utf-8") as archivo:
            self.reglas = json.load(archivo)
        self.almacenamiento = almacenamiento

    def obtenerRegla(self, operacion):
        for regla in self.reglas:
            if operacion in regla["palabras"]:
                return regla
        return None

    def ejecutar(self, operacion, parser):
        regla = self.obtenerRegla(operacion)
        if regla is None:
            raise SyntaxError(f"No existe una regla definida para '{operacion}'")

        tipo = regla["tipo"]

        if tipo == "validar":
            return self._ejecutar_validar(regla, parser)
        elif tipo == "validar_interactivo":
            return self._ejecutar_validar_interactivo()
        elif tipo == "salir":
            return self._ejecutar_salir()
        elif tipo == "mostrar":
            return self._ejecutar_mostrar(regla)
        elif tipo == "exportar":
            return self._ejecutar_exportar()
        elif tipo == "ayuda":
            return self._ejecutar_ayuda()
        else:
            raise SyntaxError(f"Tipo de regla desconocido: '{tipo}'")

    def _ejecutar_validar(self, regla, parser):
        parser.consumir("PALABRA RESERVADA")
        parser.consumir("DOS PUNTOS")

        token_valor = parser.consumir_o(regla["token_valor"])
        valor = token_valor.valor

        funcion = regla["funcion_validacion"]
        if funcion == "validacion_correo":
            errores = validacion_correo(valor)
        elif funcion == "validacion_contrasena":
            errores = validacion_contrasena(valor)
        else:
            raise SyntaxError(f"Funcion de validacion desconocida: '{funcion}'")

        if errores:
            print(f"ERRORES EN EL {regla['nombreRegla'].replace('Validar', '').replace('Verificar', '').upper()}:")
            for error in errores:
                print(f"- {error}")
            return False

        if funcion == "validacion_correo":
            print(f"CORREO VALIDO: {valor}")
            if self.almacenamiento:
                self.almacenamiento.agregar_correo(valor)
        elif funcion == "validacion_contrasena":
            print("CONTRASEÑA VALIDA")
            if self.almacenamiento:
                correo_actual = self._obtener_ultimo_correo()
                self.almacenamiento.agregar_usuario(correo_actual, valor)

        return True

    def _ejecutar_validar_interactivo(self):
        print("\n=== VALIDAR CREDENCIALES ===")

        correo = input("Correo: ").strip()
        tokens_correo, errores_lexicos = tokenizar_correo_completo(correo)
        if tokens_correo:
            print("\nTOKENS:")
            for token in tokens_correo:
                print(token)
        if errores_lexicos:
            print("\nERRORES LEXICOS:")
            for error in errores_lexicos:
                print(error)
            return None

        errores_correo = validacion_correo(correo)
        if errores_correo:
            print("\nERRORES EN EL CORREO:")
            for error in errores_correo:
                print(f"- {error}")
            return None

        print(f"\nCORREO VALIDO: {correo}")

        contrasena = input("Contraseña: ").strip()
        tokens_contrasena, errores_lexicos = tokenizar_correo_completo(contrasena)
        if tokens_contrasena:
            print("\nTOKENS:")
            for token in tokens_contrasena:
                print(token)
        if errores_lexicos:
            print("\nERRORES LEXICOS:")
            for error in errores_lexicos:
                print(error)
            return None

        errores_contrasena = validacion_contrasena(contrasena)
        if errores_contrasena:
            print("\nERRORES EN LA CONTRASEÑA:")
            for error in errores_contrasena:
                print(f"- {error}")
            return None

        print("\nCONTRASEÑA VALIDA")
        if self.almacenamiento:
            self.almacenamiento.agregar_correo(correo)
            self.almacenamiento.agregar_usuario(correo, contrasena)

        return True

    def _obtener_ultimo_correo(self):
        if self.almacenamiento:
            historial = self.almacenamiento.obtener_historial()
            if historial:
                return historial[-1]
        return "desconocido"

    def _ejecutar_salir(self):
        print("Ejecución detenida")
        return False

    def _ejecutar_mostrar(self, regla):
        accion = regla["accion"]

        if accion == "mostrar_historial":
            if not self.almacenamiento:
                print("No hay almacenamiento disponible")
                return True
            historial = self.almacenamiento.obtener_historial()
            if not historial:
                print("No hay correos en el historial")
            else:
                print("HISTORIAL DE CORREOS:")
                for i, correo in enumerate(historial, 1):
                    print(f"  {i}. {correo}")

        elif accion == "mostrar_usuarios":
            if not self.almacenamiento:
                print("No hay almacenamiento disponible")
                return True
            usuarios = self.almacenamiento.obtener_usuarios()
            if not usuarios:
                print("No hay usuarios registrados")
            else:
                print("USUARIOS REGISTRADOS:")
                for i, usuario in enumerate(usuarios, 1):
                    print(f"  {i}. Correo: {usuario['correo']} | Contraseña: {usuario['contrasena']}")

        return True

    def _ejecutar_exportar(self):
        if not self.almacenamiento:
            print("No hay almacenamiento disponible")
            return True
        ruta = "exportacion.json"
        ruta = self.almacenamiento.exportar_json(ruta)
        print(f"Datos exportados a: {ruta}")
        return True

    def _ejecutar_ayuda(self):
        print("COMANDOS DISPONIBLES:")
        for regla in self.reglas:
            palabras = ", ".join(regla["palabras"])
            print(f"  {palabras} - {regla['descripcion']}")
        return True
