
from psycopg2 import sql
from psql_connect import connect


##database_name = "climatologia_insivumeh_prod"

def create_database(database_name: str,host: str = None, user: str = None, password: str = None):
    connection=connect('postgres',host, user, password)
    try:
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
    except Exception as e:
        print(f"ERROR CREATE DATABASE: {e}")
    finally:
        cursor.close()
        connection.close()


def create_table(table_name:str,database:str=None, host: str = None, user: str = None, password: str = None):
    #table_name=_001_climatologia_ALFA_ICC
    connection=connect(database,host, user, password)
    try:
        connection.autocommit = True
        cursor=connection.cursor()
        create_table_query=f'''CREATE TABLE  {table_name} (FECHA DATE, NOMBRE_ESTACION VARCHAR(75),
                                                    CODIGO VARCHAR(25),CODIGO_INSIVUMEH VARCHAR(35),
                                                    PRECIPITACION NUMERIC(6,1),TEMPERATURA_MAXIMA NUMERIC(4,1),
                                                    TEMPERATURA_MINIMA NUMERIC(4,1),TEMPERATURA_MEDIA NUMERIC(4,1),
                                                    EVAPORACIÓN_TANQUE NUMERIC(4,1),EVAPORACION_PICHE NUMERIC(4,1),
                                                    HUMEDAD_RELATIVA NUMERIC(5,1),BRILLO_SOLAR NUMERIC(4,1),
                                                    NUBOSIDAD INT,VELOCIDAD_VIENTO NUMERIC(4,1),
                                                    DIRECCION_VIENTO NUMERIC(4,1),PRESION_ATMOSFERICA NUMERIC(6,1),
                                                    TEMPERATURA_SUELO_5CM NUMERIC(4,1),TEMPERATURA_SUELO_50CM NUMERIC(4,1),
                                                    TEMPERATURA_SUELO_100CM NUMERIC(4,1),RADIACION NUMERIC(7,4),
                                                    Latitud NUMERIC(14,10),Longitud NUMERIC(14,10),
                                                    Altitud NUMERIC(14,10),FUENTE VARCHAR(25));'''
        cursor.execute(create_table_query)
    except Exception as e:
        print(f"ERROR CREATE TABLE: {e}")
    finally:
        cursor.close()
        connection.close()