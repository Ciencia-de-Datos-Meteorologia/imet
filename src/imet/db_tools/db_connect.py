# file: db_connect.py
# author: Josué Daniel Cuzco
# author: Jorge Alejandro Rodríguez

import mysql
import pandas as pd
import mysql.connector
#
from datetime import datetime
from typing import Union, List, Tuple


def connect(host: str, user: str, password: str, database: str):

    try:
        connection = mysql.connector.connect(host=host, user=user, password=password,
                                             auth_plugin='mysql_native_password',
                                             database=database)
        return connection

    except Exception as e:
        print(f'Connection failed: {e}')
        return None


def query(querystr: str, connection: mysql.connector.MySQLConnection):

    data = pd.read_sql_query(querystr, connection)

    return data


def connect_n_query(querystr: str, host: str, user: str, password: str, database: str):

    connection = connect(host, user, password, database)
    data = query(querystr, connection)

    return data


def querybuilder(variables: Union[str, List[str]], codecol: str, datecol: str,
                 daterange: Union[datetime, Tuple[datetime, datetime]],
                 database: str = 'CLIMATOLOGIA_INSIVUMEH_PROD',
                 table: str = '001_climatologia_ALFA_ICC'):

    # column selection
    if isinstance(variables, str):
        columns = '{0}.{1}.{2}'.format(database, table, variables)
    elif isinstance(variables, list):
        variables = [datecol, codecol]+variables
        columns = ', '.join(['{0}.{1}.{2}'.format(database, table, variable)
                            for variable in variables])
    else:
        columns = '*'
    #
    column_query = 'SELECT {0} FROM {1}.{2}'.format(columns, database, table)

    # date range selection
    if isinstance(daterange, datetime):
        datefilter = "{0}.{1}.{2}='{3}'".format(
            database, table, datecol, daterange.strftime('%Y-%m-%d'))
    elif isinstance(daterange, tuple) and len(daterange) == 2:
        # date sort, just in case
        daterange_list = list(daterange)
        daterange_list.sort()
        date_start, date_end = daterange_list
        #
        datefilter = "{0}.{1}.{2} BETWEEN '{3}' AND '{4}'".format(database, table, datecol,
                                                                  date_start.strftime('%Y-%m-%d'),
                                                                  date_end.strftime('%Y-%m-%d'))
    else:
        datefilter = None
    #
    date_query = 'WHERE {0}'.format(datefilter) if datefilter is not None else ''

    # join query string
    querystr = ' '.join([column_query, date_query])

    return querystr
