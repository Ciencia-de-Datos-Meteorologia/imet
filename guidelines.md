# Lineamientos de contribución

## Formato de código:
Se utilizará como base la guía de estilo para código de Python [PEP 8](https://peps.python.org/pep-0008/). Como herramienta de formato se utilizará [YAPF](https://github.com/google/yapf/tree/main) con las configuraciones por defecto.

### Configuraciones utilizando VS-Code:
Se utilizarán las siguiente extensiones para la revisión del código:

#### [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
En el archivo de configuración de VS code `settings.json` se agregará:

```json
"pylint.args": ["--max-line-length=79"]
```

