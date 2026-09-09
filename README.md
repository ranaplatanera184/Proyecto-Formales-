# Proyecto-Formales-

Sistema de validación de credenciales implementado con conceptos de lenguajes formales y compiladores.

## Estructura del Proyecto

```
Proyecto-Formales-/
├── Token.py                        # Clase de datos para tokens
├── ImplementacionAnalisisLexico.py  # Léxico (tokenizador)
├── validaciones.py                  # Validación de credenciales
├── AnalisisSintactico.py            # Sintáctico (parser y evaluador)
├── gestor_reglas.py                 # Gestor de reglas gramaticales
├── reglas.json                      # Definición de reglas
├── main.py                          # Punto de entrada (REPL)
└── tests/                           # Tests unitarios
```

## Requisitos

- Python 3.10+
- pytest (para tests)

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>

# Navegar al directorio
cd Proyecto-Formales-

# Instalar pytest (opcional)
pip install pytest
```

## Uso

```bash
# Ejecutar el programa
python main.py

# Comandos disponibles:
# CORREO: ejemplo@dominio.com
# CONTRASEÑA: "MiContraseña123!"
# CERRAR
```

## Ejemplo de Uso

```
CREDENCIALES> CORREO: test@gmail.com

TOKENS:
Token(token=PALABRA RESERVADA, valor=CORREO)
Token(token=DOS PUNTOS, valor=:)
Token(token=CORREO, valor=test@gmail.com)

CORREO VALIDO: test@gmail.com

CREDENCIALES> CONTRASEÑA: "MiClave123!"

TOKENS:
Token(token=PALABRA RESERVADA, valor=CONTRASEÑA)
Token(token=DOS PUNTOS, valor=:)
Token(token=CADENA, valor=MiClave123!)

CONTRASEÑA VALIDA

CREDENCIALES> CERRAR

TOKENS:
Token(token=PALABRA RESERVADA, valor=CERRAR)

Ejecución detenida
```

## Ejecutar Tests

```bash
pytest tests/
```

## Arquitectura

El proyecto sigue la arquitectura clásica de un compilador:

```
[Entrada del Usuario] → [Léxico] → [Sintáctico/Evaluador] → [Resultado]
```

- **Léxico (`ImplementacionAnalisisLexico.py`)**: Convierte texto en tokens
- **Sintáctico (`AnalisisSintactico.py`)**: Valida la estructura gramatical
- **Validaciones (`validaciones.py`)**: Reglas de negocio para correo y contraseña
- **Reglas (`reglas.json`)**: Configuración de la gramática
