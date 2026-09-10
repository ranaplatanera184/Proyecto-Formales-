# Proyecto-Formales-

Intérprete del lenguaje JACE para validación de credenciales.

## Estructura del Proyecto

```
Proyecto-Formales-/
├── Token.py                        # Clase Token
├── ImplementacionAnalisisLexico.py  # Tokenizador
├── validaciones.py                  # Validación correo/contraseña
├── AnalisisSintactico.py            # Parser sintáctico
├── gestor_reglas.py                 # Gestor de reglas
├── reglas.json                      # Reglas gramaticales
├── almacenamiento.py                # Almacenamiento de datos
├── main.py                          # Punto de entrada
└── tests/                           # Tests unitarios
```

## Requisitos

- Python 3.10+

## Uso

```bash
# Modo interactivo
python main.py

# Ejecutar archivo .jace
python main.py archivo.jace

# Mostrar ayuda
python main.py --help
```

## Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `CORREO: ejemplo@uptc.edu.co` | Validar correo UPTC |
| `CONTRASEÑA: "MiContraseña123!"` | Validar contraseña |
| `VALIDAR` | Validar credenciales de forma interactiva |
| `HISTORIAL` | Mostrar correos validados |
| `USUARIOS` | Mostrar usuarios registrados |
| `EXPORTAR` | Exportar datos a JSON |
| `AYUDA` | Mostrar comandos disponibles |
| `CERRAR` | Salir del programa |

## Archivos .jace

Los archivos `.jace` contienen instrucciones del lenguaje JACE:

```
# Comentarios (se ignoran)
CORREO: juan.perez@uptc.edu.co
CONTRASEÑA: "MiClave123!"
HISTORIAL
CERRAR
```

### Formato

- Una instrucción por línea
- Líneas vacías se ignoran
- Líneas que empiecen con `#` son comentarios

### Ejemplo de ejecución

```bash
$ python main.py prueba.jace

=== Ejecutando prueba.jace ===

Línea 1: CORREO: juan.perez@uptc.edu.co
CORREO VALIDO: juan.perez@uptc.edu.co

Línea 2: CONTRASEÑA: "MiClave123!"
CONTRASEÑA VALIDA

Línea 3: HISTORIAL
HISTORIAL DE CORREOS:
  1. juan.perez@uptc.edu.co

Línea 4: CERRAR
Ejecución detenida
```

## Arquitectura

```
[Entrada] → [Léxico] → [Sintáctico] → [Ejecución]
            (Token)    (Parser)       (GestorReglas)
```

## Ejecutar Tests

```bash
python -m pytest tests/
```
