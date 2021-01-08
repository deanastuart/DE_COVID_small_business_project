import pandas as pd
#from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine

#db = SQLAlchemy(app)

def convert_time(dataframe):
    """
    Converts year, month, day columns to a datetime object and adds a date column.

    :param dataframe: dataframe with year, month, day columns
    :return: dataframe with a date column containing datetime objects
        and the year, month, day columns dropped
    """
    dataframe.replace({'month': {1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6:'06', 7:'07', 8:'08', 9:'09'},
                        'day': {1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6:'06', 7:'07', 8:'08', 9:'09'}}, inplace=True)
    dataframe['date'] = dataframe['year'].apply(str) + dataframe['month'].apply(str) + dataframe['day'].apply(str)
    dataframe['date'] = pd.to_datetime(dataframe['date'], format='%Y%m%d', utc=False)
    dataframe.drop(columns=['year', 'month', 'day'], inplace = True)
    return dataframe

def connect_sql():
    """
    Connects to SQL. Requires a username and password being set in your env.
    :return: Connection to SQL
    """
    user = os.getenv('MYSQL_user')
    pw = os.getenv('MYSQL')
    str_sql = 'mysql+mysqlconnector://' + user + ':' + pw + '@localhost/de_covid'
    engine = create_engine(str_sql)
    return engine

def write_sql(dataframe, engine, table):
    """
    Writes to SQL a database hockey and a table rosters.
    :param dataframe: Dataframe to be written
    :param engine: Connection to SQL
    :return: None
    """
    dataframe.to_sql(con=engine, name=table, if_exists='replace', index=False)
    engine.execute('ALTER TABLE ' + str(table) +  ' ADD PRIMARY KEY (loc_date(25));')
    engine.dispose()
    print('Written to SQL.')

def main():
    con = connect_sql()

    bus = pd.read_csv('Data/Womply Merchants - State - Daily.csv')
    bus = convert_time(bus)
    bus['loc_date'] = bus['statefips'].astype(str) + " " + bus['date'].astype(str)
    write_sql(bus, con, 'de_merch')

    bus_county = pd.read_csv('Data/Womply Merchants - County - Daily.csv')
    bus_county = convert_time(bus_county)
    bus_county['loc_date'] = bus_county['countyfips'].astype(str) + " " + bus_county['date'].astype(str)
    write_sql(bus_county, con, 'county_merch')

    bus_rev = pd.read_csv('Data/Womply Revenue - State - Daily.csv')
    bus_rev = convert_time(bus_rev)
    bus_rev['loc_date'] = bus_rev['statefips'].astype(str) + " " + bus_rev['date'].astype(str)
    write_sql(bus_rev, con, 'de_rev')

    bus_county_rev = pd.read_csv('Data/Womply Revenue - County - Daily.csv')
    bus_county_rev = convert_time(bus_county_rev)
    bus_county_rev['loc_date'] = bus_county_rev['countyfips'].astype(str) + " " + bus_county_rev['date'].astype(str)
    write_sql(bus_county_rev, con, 'county_rev')
    print("All tables writen to SQL")

if __name__ == "__main__":
    main()