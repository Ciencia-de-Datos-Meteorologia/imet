# imet
[I]nsivumeh [Met]eorología.
Módulo general de herramientas y automatización del Departamento de Investigación y Servicios Meteorológicos de INSIVUMEH. 

## Contribución
Para contribuir a este repositorio referirse a los [lineamientos de contribución](guidelines.md).

## Estructura

### `imet.express`
Herramientas de acceso rápido, para realizar mapas en una línea de código, generar resúmenes de datos: Entradas: raster, tablas, listas, Salidas: Mapas, gráficos, tablas de resumen.

### `imet.db_tools`
Herramientas para contectar con la base de datos, descargar datos en distintos formantos, generar querys y manipular la base de datos.

### `imet.plot`
Herramientas para realizar mapas usando `matplotlib`, crearan objetos de tipo `pyplot` y agregarán capas a estos, se plotearán puntos, shapefiles, rasters.

### `imet.raster`
Herramientas de manipulación de rasters. Unificar rasters en Xarrays, exportar .nc y .tif, operar rasters, interpolar, samplear, entre otros.

