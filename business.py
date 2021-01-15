import pandas as pd
import os
from sqlalchemy import create_engine

def get_data():
    url='https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/'
    files = {'Womply_Merchants_County_Daily.csv':'Womply%20Merchants%20-%20County%20-%20Daily.csv',
            'Womply_Merchants_State_Daily.csv':'Womply%20Merchants%20-%20State%20-%20Daily.csv',
            'Womply_Revenue_County_Daily.csv': 'Womply%20Revenue%20-%20County%20-%20Daily.csv',
            'Womply_Revenue_State_Daily.csv': 'Womply%20Revenue%20-%20State%20-%20Daily.csv'}
    for file in files:
        dataframe = pd.read_csv(url + files[file])
        dataframe.to_csv('Data/update/' + file, index=False)
        print('Written to file')

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
    Connects to SQL. Requires SQL credentials being set in your env.

    :return: Connection to SQL
    """
    sql = os.getenv('SQL')
    str_sql = 'mysql+mysqlconnector://' + sql
    engine = create_engine(str_sql)
    return engine

def write_sql(dataframe, engine, table):
    """
    Writes to SQL a database
    :param dataframe: Dataframe to be written
    :param engine: Connection to SQL
    :return: None
    """
    print(table)
    print(engine.has_table(table))
    if engine.has_table(table):
        engine.execute('DROP TABLE ' + table + ';')
    dataframe.to_sql(table, engine, index=False)
    engine.execute('ALTER TABLE ' + table +  ' ADD PRIMARY KEY (loc_date(25));')
    engine.execute('ALTER TABLE ' + table + ' MODIFY COLUMN date DATE;')
    engine.dispose()
    print('Written to SQL.')

def setup():
    """
    Writes initial files to the SQL database. Only needs to be run when the database is
    empty.

    :return: None
    """
    con = connect_sql()

    bus = pd.read_csv('Data/Womply_Merchants_State_Daily.csv')
    bus = convert_time(bus)
    bus['loc_date'] = bus['statefips'].astype(str) + " " + bus['date'].astype(str)
    write_sql(bus, con, 'state_merch_temp')
    write_sql(bus, con, 'state_merch')

    bus_county = pd.read_csv('Data/Womply_Merchants_County_Daily.csv')
    bus_county = convert_time(bus_county)
    bus_county['loc_date'] = bus_county['countyfips'].astype(str) + " " + bus_county['date'].astype(str)
    write_sql(bus_county, con, 'county_merch_temp')
    write_sql(bus_county, con, 'county_merch')

    bus_rev = pd.read_csv('Data/Womply_Revenue_State_Daily.csv')
    bus_rev = convert_time(bus_rev)
    bus_rev['loc_date'] = bus_rev['statefips'].astype(str) + " " + bus_rev['date'].astype(str)
    write_sql(bus_rev, con, 'state_rev_temp')
    write_sql(bus_rev, con, 'state_rev')

    bus_county_rev = pd.read_csv('Data/Womply_Revenue_County_Daily.csv')
    bus_county_rev = convert_time(bus_county_rev)
    bus_county_rev['loc_date'] = bus_county_rev['countyfips'].astype(str) + " " + bus_county_rev['date'].astype(str)
    write_sql(bus_county_rev, con, 'county_rev_temp')
    write_sql(bus_county_rev, con, 'county_rev')


def main():
    """
    Gets updated data and adds it to the correct tables.

    :return: None
    """
    con = connect_sql()

    get_data()

    bus = pd.read_csv('Data/update/Womply_Merchants_State_Daily.csv')
    bus = convert_time(bus)
    bus['loc_date'] = bus['statefips'].astype(str) + " " + bus['date'].astype(str)
    write_sql(bus, con, "state_merch_temp")
    con.execute('INSERT IGNORE INTO state_merch SELECT * FROM state_merch_temp')

    bus_county = pd.read_csv('Data/update/Womply_Merchants_County_Daily.csv')
    bus_county = convert_time(bus_county)
    bus_county['loc_date'] = bus_county['countyfips'].astype(str) + " " + bus_county['date'].astype(str)
    write_sql(bus_county, con, 'county_merch_temp')
    con.execute('INSERT IGNORE INTO county_merch SELECT * FROM county_merch_temp')
    
    bus_rev = pd.read_csv('Data/update/Womply_Revenue_State_Daily.csv')
    bus_rev = convert_time(bus_rev)
    bus_rev['loc_date'] = bus_rev['statefips'].astype(str) + " " + bus_rev['date'].astype(str)
    write_sql(bus_rev, con, 'state_rev_temp')
    con.execute('INSERT IGNORE INTO state_rev SELECT * FROM state_rev_temp')

    bus_county_rev = pd.read_csv('Data/update/Womply_Revenue_County_Daily.csv')
    bus_county_rev = convert_time(bus_county_rev)
    bus_county_rev['loc_date'] = bus_county_rev['countyfips'].astype(str) + " " + bus_county_rev['date'].astype(str)
    write_sql(bus_county_rev, con, 'county_rev_temp')
    con.execute('INSERT IGNORE INTO county_rev SELECT * FROM county_rev_temp')

    print("All tables writen to SQL")

if __name__ == "__main__":
    #setup()
    main()