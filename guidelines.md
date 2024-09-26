# Lineamientos de contribución
Para mantener una estructura estándar dentro de toda la biblioteca, se deben tomar en cuenta algunos lineamientos. Para solicitar pull requests estos lineamientos deberán ser tomados en cuenta.

## Docstrings e idioma
Todos los módulos deberán ir respectivamente documentados. El idioma utilizado para los docstrings será inglés y se utilizará la [guía de estilo de numpy](https://numpydoc.readthedocs.io/en/latest/format.html) para estandarizar el estilo de los `docstrings` además de permitir automatizar la generación de la página de documentación.

## Formato de código
Se utilizará como base la guía de estilo para código de Python [PEP 8](https://peps.python.org/pep-0008/). Como herramienta de formato se utilizará [YAPF](https://github.com/google/yapf/tree/main) con las configuraciones por defecto.

### Configuraciones utilizando VS-Code:
Se utilizarán las siguientes extensiones para la revisión del código:

#### [yapf](https://marketplace.visualstudio.com/items?itemName=eeyore.yapf)
Esta extensión realiza un formato automático de código basado en PEP8 (u otros estándares). En el archivo de configuración de VS code `settings.json` se agregará:

```json
"yapf.args": ["--style={based_on_style: pep8}"],
"editor.defaultFormatter": "eeyore.yapf",
"notebook.defaultFormatter": "eeyore.yapf",
```

#### [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
Esta extensión permite mostrar sugerencias sobre la calidad y estilo del código.
En el archivo de configuración de VS code `settings.json` se agregará:

```json
"pylint.args": ["--max-line-length=79"],
"pylint.lintOnChange": true,
```

### Configuraciones utilizando nvim:
Se utilizarán las siguientes extensiones para la revisión del código:

#### Extensiones sugeridas:

##### [linux-cultist/venv-selector.nvim](https://github.com/linux-cultist/venv-selector.nvim)

## Testing scripts
Todos los módulos, clases y métodos agregados a este paquete deben de contener funciones de prueba `test functions`. Se utilizará el framework de [`pytest`](https://docs.pytest.org/en/8.2.x/) para realizarlos.

## Estructura de desarrollo

## Configuraciones del paquete

### Manejo de dependencias
Cuando un nuevo módulo sea agregado, si este tiene depencencias, estas deberán ser añadidas al `setup.py` del proyecto. Dependiendo de la jerarquía del módulo se deberán añadir como dependencias opcionales u obligatorias.

En esta [guía](https://setuptools.pypa.io/en/latest/userguide/dependency_management.html) se detalla como se debe llevar un manejo de dependencias correcto en la realización de un paquete.


