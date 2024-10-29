import psycopg2
import pandas as pd 

from datetime import datetime
from typing import Union, List, Tuple

import yaml 
import os


def connect(database: str = None, host: str = None, user: str = None, password: str = None,
            savecreds: bool = False):
    """
    Connect to a database with  POstgreSQL.
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
            print(host, user, password)

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
        if database is not None:
            connection = psycopg2.connect(host=host, user=user, password=password,database=database)
        return connection

    except Exception as ee:
        print(f'Connection failed: {ee}')
        return None
    
def query(querystr:str, connection: psycopg2.extensions.connection):
    """Send a query to a PostgreSQL database with a previously established connection

    Parameters
    ----------
    querystr : str
        
    connection : psycopg2.extensions.connection
        
    Returns
    -------
    DataFrame
        DataFrame with the results returned by the executed query

    """


    data=pd.read_sql_query(querystr, connection)
    return data
   
def connect_n_query(querystr:str, host:str, user:str, password:str, database:str):
    """Function to establish a connection with a PostgreSQL database and send a query

    Parameters
    ----------
    querystr : str
        query to send to the database
    host : str
        The host of the postgresql database
    user : str
        Name of the user with permissions on the database
    password : str
        Password of the user with permissions on the database
    database : str
        Name of the PostreSQL database

    Returns
    -------
    DataFrame
        DataFrame with the results returned by the executed query
    """
    connection=connect(database, host, user, password)
    data=query(querystr, connection)

    return data

def querybuilder(variables: Union[str, List[str]], codecol:str, datecol:str,
                  daterange:Union[datetime, Tuple[datetime, datetime]], table:str):
    #column selection 
    if isinstance(variables, str):
        print(variables)
        columns='{0}.{1}'.format(table, variables)
    elif isinstance(variables, list):
        variables=[datecol, codecol]+variables
        print(variables)
        columns=','.join(['{0}.{1}'.format(table, variable) for variable in variables])
    else:
        columns='*'

    #query PostgreSQL, SELECT column1, column2, ... FROM table_name <condition>;
    column_query='SELECT {0} FROM {1}'.format(columns, table)

    #date range selection
    if isinstance(daterange, datetime):
        datefilter="{0}.{1}='{2}'". format(table, datecol, daterange.strftime('%Y-%m-%d'))
    elif isinstance(daterange, tuple) and len(daterange)==2:
        #date sort, just in case
        daterange_list=list(daterange)
        daterange_list.sort()
        date_start, date_end=daterange_list
        #
        datefilter="{0}.{1} BETWEEN '{2}' AND '{3}'".format(table, datecol, date_start.strftime('%Y-%m-%d'), date_end.strftime('%Y-%m-%d'))
    else:
        datefilter=None
    #
    date_query=' WHERE {0}'.format(datefilter) if datefilter is not None else ' '

    #join query string 
    querystr=''.join([column_query, date_query])+';'

    return querystr

def queryFilter(colfilter:str, codes:Union[str, List[str]], variables: Union[str, List[str]], codecol:str, datecol:str,
                  daterange:Union[datetime, Tuple[datetime, datetime], List[datetime]], table:str):
    """Generates a string corresponding to a query in PostreSQL

    Parameters
    ----------
    colfilter : str
        column to filter
    codes : Union[str, List[str]]
        specific values ​​to filter from the selected column in colfilter 
    variables : Union[str, List[str]]
        variables of columns to display in the resulting data
    codecol : str
        Name of the column corresponding to the codes
    datecol : str
        Name of the column corresponding to the dates
    daterange : Union[datetime, Tuple[datetime, datetime], List[datetime]]
        Date values to filter can include a range, a list of dates, or a specific date
    table : str, optional
        Name of the table to search for in the database, by default '_001_climatologia_ALFA_ICC'

    Returns
    -------
    String
        A query in Postgresql 
    """
    
    #column selection 
    if isinstance(variables, str): #one column
        #format whitt name of table and name of column
        columns='{0}.{1}'.format(table, variables)
    elif isinstance(variables, list): #list of columns
        #add date and code columns
        variables=[datecol, codecol]+variables
        columns=','.join(['{0}.{1}'.format(table, variable) for variable in variables])
    else:
        #all columns
        columns='*'

    #query PostgreSQL, SELECT column1, column2, ... FROM table_name <condition>;
    column_query='SELECT {0} FROM {1}'.format(columns, table)

    #filter by code or a selected column in variable "colfilter"
    if isinstance(codes, str): #one code
        allcodes="'{0}'".format(codes)
    elif isinstance(codes, list): #list of codes
        allcodes=','.join(["'{0}'".format(code) for code in codes])
    else: 
        allcodes=None
    
    
    ## example of use: SELECT * FROM _001_climatologia_ALFA_ICC  WHERE codigo in ('INS130101CV','INS140301CV');
    code_query=' WHERE {0} IN ({1})'.format(colfilter, allcodes) if allcodes is not None else ' '


    #date range selection
    if isinstance(daterange, datetime):
        datefilter="{0}.{1}='{2}'". format(table, datecol, daterange.strftime('%Y-%m-%d'))
    elif isinstance(daterange, tuple) and len(daterange)==2:
        #date sort, just in case
        daterange_list=list(daterange)
        daterange_list.sort()
        date_start, date_end=daterange_list
        #between two dates (daterange)
        datefilter="{0}.{1} BETWEEN '{2}' AND '{3}'".format(table, datecol, date_start.strftime('%Y-%m-%d'), date_end.strftime('%Y-%m-%d'))
    elif isinstance(daterange, list):
        #verify if all elements are datetime
        if all(isinstance(date, datetime) for date in daterange):
            dates = ', '.join("'{0}'".format(date.strftime('%Y-%m-%d')) for date in daterange)
            datefilter = "{0}.{1} IN ({2})".format(table, datecol, dates)
        else:
            datefilter = None
    else:
        datefilter=None

    #verify if datefilter is not None
    if datefilter is not None:
        if allcodes is not None:
            date_query='AND {0}'.format(datefilter)
        else:
            #if allcodes is None the query is only the datefilter, starts with WHERE
            date_query=' WHERE {0}'.format(datefilter)
    else:
        date_query=''
    
    #join all query strings
    querysrt=''.join([column_query,code_query,date_query])+';'


    return querysrt








