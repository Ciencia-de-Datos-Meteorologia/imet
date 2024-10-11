# file: db_connect.py
# author: Josué Daniel Cuzco
# author: Jorge Alejandro Rodríguez

import os
import yaml
import pandas as pd
import mysql.connector
#
from datetime import datetime
from typing import Union, List, Tuple


def connect(database: str = None, host: str = None, user: str = None, password: str = None,
            savecreds: bool = False):
    """
    Connect to a database with MySQL.
    Credentials may be given as function arguments, terminal input
    or fetched from a configuration file.

    Parameters
    ----------
    database : str, default None
        Name of the database to connect to.
    host : str, default None
    user : str, default None
    password : str, default None
    savecreds : str, default False
        Save credentials to a configuration file.

    Returns
    -------
    MySQLConnection
    """

    # credentials file
    config_file = os.path.expanduser("~/.config/imet/dbcreds.yaml")

    # any of the credentials not provided, try to read credentials file
    if any(cred is None for cred in [host, user, password]):
        # creds file exists
        if os.path.exists(config_file):
            # load credentials
            with open(config_file) as cred_f:
                user_conf = yaml.safe_load(cred_f)

            # put credentials into variables
            host = user_conf['credentials']['host']
            user = user_conf['credentials']['username']
            password = user_conf['credentials']['password']

        # creds file doesn't exist
        else:
            # ask for credentials
            print('Credentials file NOT found')
            attempt = input('Enter connection credentials? [y/n]: ')
            # input credentials
            if attempt.lower().__contains__('y'):
                host = input('Host: ')
                user = input('Username: ')
                password = input('Password: ')
                # ask to save credentials
                if not savecreds:
                    savecreds = input('Save credentials? [y/n]: ').lower().__contains__('y')
                else:
                    print('Credentials will be saved')
            # no credentials error
            else:
                raise ValueError('Credentials NOT given')

    # check for database name
    if database is None:
        # ask for database
        print('Database was not given')
        attempt = input('Enter database name? [y/n]: ')
        # input database
        if attempt.lower().__contains__('y'):
            database = input('Database: ')
        else:
            print('Continuing without a database')

    # save credentials
    if savecreds:
        # check if config dir exists
        config_dir = os.path.split(config_file)[0]
        # create config dir
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        # credentials dictionary
        cred_dict = {'credentials':{'host':host, 'username':user, 'password':password}}

        # save credentials
        with open(config_file, 'w') as cred_f:
            yaml.dump(cred_dict, cred_f)

    # connect
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password,
                                             auth_plugin='mysql_native_password',
                                             database=database)
        return connection

    except Exception as ee:
        print(f'Connection failed: {ee}')
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
