import pandas as pd
#
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd
#
from . import db_connect as dbc


def data_obsmonth(month: datetime, variable: str,
                  codecol: str = 'CODIGO', datecol: str = 'FECHA',
                  database: str = 'CLIMATOLOGIA_INSIVUMEH_PROD',
                  table: str = '001_climatologia_ALFA_ICC',
                  host: str = None, user: str = None,
                  password: str = None):

    # yesterday, limit for obs data
    yesterday = datetime.today()-rd(days=1)

    # start month at day 1
    datestart = month.replace(day=1)
    # end month at its final day, or yesterday if current month
    dateend = datestart+rd(months=1, days=-1)
    dateend = dateend if dateend < yesterday else yesterday

    # date range tuple
    daterange = (datestart, dateend)

    # build query
    query = dbc.querybuilder(variable, codecol, datecol, daterange, database, table)

    # request data
    data = dbc.connect_n_query(query, host, user, password, database)

    # group data by station and apply operation
    if variable in ['PRECIPITACIÓN']:
        data = data.groupby(codecol).sum(min_count=1)
    else:
        data = data.groupby(codecol).mean()

    return data


def data_clima(month: datetime, variable: str, limit: int = None, climayears: tuple = (1991, 2020),
               codecol: str = 'CODIGO', datecol: str = 'FECHA',
               database: str = 'CLIMATOLOGIA_INSIVUMEH_PROD',
               table: str = '001_climatologia_ALFA_ICC',
               host: str = None, user: str = None,
               password: str = None):

    # get limit day of the month
    if limit is None:
        # yesterday, limit for obs data
        yesterday = datetime.today()-rd(days=1)

        if month.month == yesterday.month:
            limit = yesterday.day
        else:
            limit = (month.replace(day=1)+rd(months=1, days=-1)).day

    # climatology
    climayears = list(climayears)
    climayears.sort()
    climastart, climaend = climayears

    # get a connection
    connection = dbc.connect(host, user, password, database)

    # loop over climatology
    data = pd.DataFrame()
    for year in range(climastart, climaend+1):
        datestart = datetime(year, month.month, 1)
        dateend = datetime(year, month.month, limit)
        daterange = (datestart, dateend)

        # build yearly query
        query = dbc.querybuilder(variable, codecol, datecol, daterange, database, table)

        # request yearly data
        ydata = dbc.query(query, connection)

        # group data by station and apply operation
        if variable in ['PRECIPITACIÓN']:
            ydata = ydata.groupby(codecol).sum(min_count=1)
        else:
            ydata = ydata.groupby(codecol).mean()

        ydata.rename(columns={variable: year}, inplace=True)

        data = pd.merge(data, ydata, how='outer', left_index=True, right_index=True)

    clima = data.mean(axis=1, skipna=True)

    return clima
