# Proyecto-Formales-

Sistema de validación de credenciales implementado con conceptos de lenguajes formales y compiladores.

## Estructura del Proyecto

```
Proyecto-Formales-/
├── Token.py                        # Clase de datos para tokens
├── ImplementacionAnalisisLexico.py  # Léxico (tokenizador)
├── validaciones.py                  # Validación de credenciales
├── AnalisisSintactico.py            # Sintáctico (parser genérico)
├── gestor_reglas.py                 # Gestor de reglas con ejecución por tipo
├── almacenamiento.py                # Almacenamiento en memoria (historial/usuarios)
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
```

## Comandos Disponibles

| Comando | Descripción |
|---|---|
| `VALIDAR` | Valida correo y contraseña de forma interactiva |
| `CORREO: valor` | Valida un correo directamente |
| `CONTRASEÑA: "valor"` | Valida una contraseña directamente |
| `HISTORIAL` | Muestra los correos validados exitosamente |
| `USUARIOS` | Muestra los usuarios con correo y contraseña validados |
| `EXPORTAR` | Exporta historial y usuarios a un archivo JSON |
| `AYUDA` | Muestra la lista de comandos disponibles |
| `CERRAR` | Detiene la ejecución del programa |

## Ejemplo de Uso

```
=== SISTEMA DE VALIDACION DE CREDENCIALES ===
Comandos disponibles:
  VALIDAR                  - Validar correo y contraseña
  CORREO: ejemplo@dominio.com
  CONTRASEÑA: "MiContraseña123!"
  HISTORIAL
  USUARIOS
  EXPORTAR
  AYUDA
  CERRAR
==============================================

SISTEMA> validar

=== VALIDAR CREDENCIALES ===
Correo: juan.perez@uptc.edu.co
Contraseña: MiClave123!

CORREO VALIDO: juan.perez@uptc.edu.co
CONTRASEÑA VALIDA

SISTEMA> historial

HISTORIAL DE CORREOS:
  1. juan.perez@uptc.edu.co

SISTEMA> usuarios

USUARIOS REGISTRADOS:
  1. Correo: juan.perez@uptc.edu.co | Contraseña: MiClave123!

SISTEMA> ayuda

COMANDOS DISPONIBLES:
  VALIDAR - Valida correo y contrasena de forma interactiva
  CORREO - Valida el formato de un correo electronico
  CONTRASEÑA - Verifica la fortaleza de una contrasena
  CERRAR - Detiene la ejecucion del programa
  HISTORIAL - Muestra los correos validados exitosamente
  USUARIOS - Muestra los usuarios con correo y contrasena validados
  EXPORTAR - Exporta historial y usuarios a un archivo JSON
  AYUDA - Muestra la lista de comandos disponibles

SISTEMA> cerrar

Ejecución detenida
```

## Ejecutar Tests

```bash
pytest tests/
```

## Arquitectura

El proyecto sigue la arquitectura clásica de un compilador:

```
[Entrada del Usuario] → [Léxico] → [Sintáctico] → [Gestor de Reglas] → [Resultado]
                                                      ↓
                                               [Almacenamiento]
```

- **Léxico (`ImplementacionAnalisisLexico.py`)**: Convierte texto en tokens
- **Sintáctico (`AnalisisSintactico.py`)**: Parser genérico que delega al gestor de reglas
- **Gestor de Reglas (`gestor_reglas.py`)**: Ejecuta operaciones según el tipo de regla
- **Validaciones (`validaciones.py`)**: Reglas de negocio para correo y contraseña
- **Almacenamiento (`almacenamiento.py`)**: Guarda historial y usuarios en memoria
- **Reglas (`reglas.json`)**: Configuración de la gramática y comandos

### Tipos de Regla

| Tipo | Descripción | Ejemplo |
|---|---|---|
| `validar` | Consume `: valor` y ejecuta validación | CORREO, CONTRASEÑA |
| `validar_interactivo` | Pide correo y contraseña por stdin | VALIDAR |
| `salir` | Detiene el REPL | CERRAR |
| `mostrar` | Muestra datos del almacenamiento | HISTORIAL, USUARIOS |
| `exportar` | Exporta datos a JSON | EXPORTAR |
| `ayuda` | Genera lista de comandos desde reglas.json | AYUDA |
