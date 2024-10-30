import pandas as pd
#
from datetime import datetime
from typing import Tuple,List
from dateutil.relativedelta import relativedelta 
#

import psql_connect as dbc



def data_groupby(codes:str, variables: str, daterange:Tuple[datetime, datetime], frequency:str='ME', codecol: str = 'codigo',datecol: str = 'fecha',precipcol: str = 'precipitaciÓn'):
    
    # Resumen de las frecuencias
    # 'D': Diario
    # 'W': Semanal
    # 'M': Mensual
    # 'Q': Trimestral
    # 'Y': Anual

    # 'W-Mon': Weekly frequency, starting on Monday.
    # 'W-Tue': Weekly frequency, starting on Tuesday.
    # 'W-Wed': Weekly frequency, starting on Wednesday.
    # 'W-Thu': Weekly frequency, starting on Thursday.
    # 'W-Fri': Weekly frequency, starting on Friday.
    # 'W-Sat': Weekly frequency, starting on Saturday.
    # 'W-Sun': Weekly frequency, starting on Sunday.

    #call to filterdata
    data=filterdata(codecol,codes, variables, daterange)
    #get column names
    columns_names = data.columns.tolist()
    #convert column date to datetime
    data[datecol] = pd.to_datetime(data[datecol], errors='coerce')

    #exclude colums to search for
    exclude_cols = [datecol, codecol, precipcol]

    # Initialize agg_funcs
    agg_funcs = {}

    # if precipitacion column exists in data, make it sum
    if precipcol in data.columns:
        agg_funcs[precipcol] = (precipcol, 'sum')

   
    for col in columns_names:
        if col in data.columns and col not in exclude_cols:
            if pd.api.types.is_numeric_dtype(data[col]):  
                agg_funcs[col] = (f'{col}', 'mean')
            else:
                agg_funcs[col] = (f'{col}', 'first')

    result_data = data.groupby([codecol, pd.Grouper(key=datecol, freq=frequency)]).agg(fecha_inicio=(datecol, 'min'),  # Fecha de inicio
    fecha_fin=(datecol, 'max'),**agg_funcs).reset_index()
    result_data = result_data.drop(columns=datecol)

    return result_data
def iterar_fechas(daterange: Tuple[datetime, datetime], delta: relativedelta) -> List[Tuple[datetime, datetime]]:
    fecha_inicio, fecha_fin = daterange
    fecha_actual = fecha_inicio
    rangos = []  # Lista para almacenar los rangos de fechas

    while fecha_actual <= fecha_fin:
        range_start = fecha_actual
        fecha_actual += delta
        range_end = fecha_actual
        
        if range_end > fecha_fin:
            range_end = fecha_fin
        
        timerange = (range_start, range_end)
        rangos.append(timerange)  # Agregar el rango a la lista

    return rangos

def groupby_timedelta(codes:str, variables: str, daterange:Tuple[datetime, datetime], frecuency:relativedelta, 
                      codecol: str = 'codigo',datecol: str = 'fecha',precipcol: str = 'precipitaciÓn'):
    
    rangos=iterar_fechas(daterange, frecuency)
    resultados = []
    for rango in rangos: 
        fecha_inicio, fecha_fin = rango
        data = filterdata(codecol, codes, variables, rango)
        exclude_cols = [datecol, codecol, precipcol]
    
        if precipcol in data.columns:
            agg_dict = {precipcol: 'sum'}  
            for col in data.columns:
                if col in data.columns and col not in exclude_cols:
                    if pd.api.types.is_numeric_dtype(data[col]):
                        agg_dict[col] = 'mean'
                    else:
                        agg_dict[col] = 'first' 

            data = data.groupby(codecol).agg(agg_dict).reset_index()
            data['fecha_inicio'] = fecha_inicio
            data['fecha_fin'] = fecha_fin
            resultados.append(data)
    resultado_final = pd.concat(resultados, ignore_index=True)
    return resultado_final
      


def filterdata(colfilter:str=None, codes:str=None,variables:str=None, daterange:datetime=None, 
               codecol: str = 'codigo', datecol: str = 'fecha',database:str='climatologia_insivumeh_prod',table:str='_001_climatologia_ALFA_ICC',
               host : str = None, user: str = None,
               password: str = None):
    """
    filterdata its a function that filters data from a PostgreSQL database by a set of parameters, for default it returns all data. 

    Parameters
    ----------
    colfilter: str, optional
        column to filter, by default None
    codes : str, optional
        specific values ​​to filter from the selected column in colfilter , by default None
    variables : str, optional
        variables of columns to display in the resulting data, by default None
    daterange : datetime, optional
        Date values to filter can include a range, a list of dates, or a specific date, by default None
    codecol : str, optional
        Name of the column corresponding to the codes, by default 'codigo'
    datecol : str, optional
        Name of the column corresponding to the dates, by default 'fecha'
    database : str, optional
        Name of the database to filter to, by default 'climatologia_insivumeh_prod'
    host : str, optional
        Name of the host, by default None
    user : str, optional
        Name of the user with permissions on the database, by default None
    password : str, optional
        by default None
    group : str, optional
        _description_, by default None

    Returns
    -------
    Dataframe
        DataFrame with the filtered results from the database.
    """

    query=dbc.queryFilter(colfilter,codes, variables, codecol, datecol, daterange, table)

    #request data
    data= dbc.connect_n_query(query, host, user, password, database)
    return data

def main():

    # variables=['precipitaciÓn','nubosidad','latitud', 'codigo_insivumeh']
    # codes=["INS190301CV","INS131501CV"]
    # month=datetime(2024, 9, 1)
    # codecol='codigo'
    # #resultdata=data_month(month, codes, variables)
    # result=data_groupby("INS190301CV", variables, (datetime(2022, 1, 1), datetime(2024, 6, 1)), frequency='Y')
    # print(result)

    #https://pandas.pydata.org/pandas-docs/version/1.3.1/getting_started/intro_tutorials/09_timeseries.html
    #https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.core.groupby.DataFrameGroupBy.agg.html

    rango = (datetime(2022, 1, 1), datetime(2024, 6, 1))
    variables=['precipitaciÓn','nubosidad','latitud', 'nombre_estaciÓn']
    delta = relativedelta(months=3, days=10)  # Cambiar cada 3 meses y 10 días
    codes=["INS190301CV","INS131501CV"]
    #groupby_timedelta("INS190301CV", variables, rango, delta)
    data=groupby_timedelta(codes, variables, rango, delta)
    print(data)

    
   
    


if __name__ == "__main__":
    main()
