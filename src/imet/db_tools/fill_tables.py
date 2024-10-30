import psycopg2
import pandas as pd 
import datetime as dt
import numpy as np
from psql_connect import connect



def fill_tablebyDate(fecha_formato:str=None, database:str=None, ruta:str='../base_datos_completa.csv', host: str = None, user: str = None, password: str = None):
    #table_name=_001_climatologia_ALFA_ICC
    connection=connect(database,host, user, password)
    cursor = connection.cursor()
    df_data = pd.read_csv(ruta)
    if fecha_formato is not None:
        filtro_fecha = df_data['FECHA'] >= fecha_formato
        df_data = df_data[filtro_fecha]

    df_data.reset_index(inplace=True)  # Reiniciar el índice
    df_data = df_data.replace(np.nan, None)  # Reemplazar NaN por None
    print(df_data)


    query_insert_data = f"""INSERT INTO {database} (FECHA,CODIGO,
                                    CODIGO_INSIVUMEH,NOMBRE_ESTACIÓN,  
                                                            PRECIPITACIÓN,TEMPERATURA_MÁXIMA,
                                                            TEMPERATURA_MÍNIMA,TEMPERATURA_MEDIA,
                                                            HUMEDAD_RELATIVA,
                                                            EVAPORACIÓN_TANQUE,EVAPORACIÓN_PICHE,
                                                            BRILLO_SOLAR,NUBOSIDAD,
                                                            VELOCIDAD_VIENTO,DIRECCIÓN_VIENTO,
                                                            PRESIÓN_ATMOSFÉRICA,TEMPERATURA_SUELO_5CM,
                                                            TEMPERATURA_SUELO_50CM,TEMPERATURA_SUELO_100CM,
                                                            RADIACIÓN,LATITUD,
                                                            LONGITUD,ALTITUD,
                                                            FUENTE) 
                                                            VALUES(%s,%s,%s,
                                                                    %s,%s,%s,
                                                                    %s,%s,%s,
                                                                    %s,%s,%s,
                                                                    %s,%s,%s,
                                                                    %s,%s,%s,
                                                                    %s,%s,%s,
                                                                    %s,%s,%s)"""


    ## cliclo para subir los registros uno a uno
    for index,row in df_data.iterrows():
    # Convertir todos los valores a tipos nativos de Python
        variables = [
            row['FECHA'],
            row['CODIGO'],
            row['CODIGO_INSIVUMEH'],
            row['NOMBRE_ESTACIÓN'],
            row['PRECIPITACIÓN'],
            row['TEMPERATURA_MÁXIMA'],
            row['TEMPERATURA_MÍNIMA'],
            row['TEMPERATURA_MEDIA'],
            row['HUMEDAD_RELATIVA'],
            row['EVAPORACIÓN_TANQUE'],
            row['EVAPORACIÓN_PICHE'],
            row['BRILLO_SOLAR'],
            row['NUBOSIDAD'],
            row['VELOCIDAD_VIENTO'],
            row['DIRECCIÓN_VIENTO'],
            row['PRESIÓN_ATMOSFÉRICA'],
            row['TEMPERATURA_SUELO_5CM'],
            row['TEMPERATURA_SUELO_50CM'],
            row['TEMPERATURA_SUELO_100CM'],
            row['RADIACIÓN'],
            float(row['LATITUD']) if pd.notna(row['LATITUD']) else None,
            float(row['LONGITUD']) if pd.notna(row['LONGITUD']) else None,
            row['ALTITUD'],
            row['FUENTE']
        ]
        cursor.execute(query_insert_data, variables)
        connection.commit()



def delete_data( database:str=None,fecha_formato:str=None,columnDelete:str='FECHA', host: str = None, user: str = None, password: str = None):
    #  query de borrado de datos 
    connection=connect(database,host, user, password)
    if fecha_formato is None:
        query_delete = "DELETE FROM {0};".format(database)
    else:
        query_delete ="DELETE FROM {0} where {1} >= {2};".format(database,columnDelete,fecha_formato)
    cursor = connection.cursor()
    print(query_delete)
    cursor.execute(query_delete)
    connection.commit()


def reset_last15days(database:str=None, ruta:str='../base_datos_completa.csv', host: str = None, user: str = None, password: str = None):
    now = dt.datetime.now()
    fecha_formato = (now - dt.timedelta(days=15)).strftime("%Y-%m-%d")
    delete_data(database,fecha_formato,host=host,user=user,password=password)
    fill_tablebyDate(fecha_formato,database,ruta,host=host,user=user,password=password)






