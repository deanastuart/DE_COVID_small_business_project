import matplotlib.pyplot as plt
import pandas as pd
import os
from sqlalchemy import create_engine
import matplotlib.cm as cm
from mpldatacursor import datacursor


def connect_sql():
    """
    Connects to SQL. Requires SQL credentials being set in your env.

    :return: Connection to SQL
    """
    sql = os.getenv('SQL')
    str_sql = 'mysql+mysqlconnector://' + sql
    engine = create_engine(str_sql)
    return engine

def get_state_data():
    """
    Gets merchant and revenue data from SQL for Delaware

    :return: Dataframes of merchant and revenue data for the state
    """
    con = connect_sql()
    de_merch = pd.read_sql('select date, merchants_all from state_merch where statefips = 10;',con)
    de_rev = pd.read_sql('select date, revenue_all from state_rev where statefips = 10', con)
    return de_merch, de_rev

def get_county_merch():
    """
    Gets merchant data from SQL for each Delaware county

    :return: A dataframe for each county
    """
    con = connect_sql()
    Kent_m = pd.read_sql('select date, merchants_all from county_merch where countyfips = 10001;', con)
    NCC_m = pd.read_sql('select date, merchants_all from county_merch where countyfips = 10003;', con)
    Sussex_m = pd.read_sql('select date, merchants_all from county_merch where countyfips = 10005;', con)
    return Kent_m, NCC_m, Sussex_m

def get_county_rev():
    """
    Gets revenue data from SQL for each Delaware county

    :return: A dataframe for each county
    """
    con = connect_sql()
    Kent_r = pd.read_sql('select date, revenue_all from county_rev where countyfips = 10001;', con)
    NCC_r = pd.read_sql('select date, revenue_all from county_rev where countyfips = 10003;', con)
    Sussex_r = pd.read_sql('select date, revenue_all from county_rev where countyfips = 10005;', con)
    return Kent_r, NCC_r, Sussex_r

def get_restrictions():
    """
    Gets dataframe of restrictions. Creates of list of lists.


    :return: A list of lists. First list is dates in ascending order.
    The second list is the number of times the data appears.
    """
    con = connect_sql()
    restrict = pd.read_sql('select * from mitigation;', con)
    restriction = [[],[]]
    for index, row in restrict.iterrows():
        date = row['Start']
        if index == 0 or date != restriction[0][0]:
            restriction[0].insert(0, date)
            restriction[1].insert(0, 1)
        else:
            restriction[1][0] += 1
    return restriction

def graph_state_data(df1, df2):
    """
    Graphs to lines based on the dataframes.

    :param df1: Dataframe
    :param df2: Dataframe
    :return: None
    """
    merch, = plt.plot(df1['date'], df1['merchants_all']* 100)
    rev, = plt.plot(df2['date'], df2['revenue_all'] * 100)
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.legend([merch, rev], ['Merchant', 'Revenue'])
    plt.show()

def graph_county(Kent, NCC, Sussex, column, restrictions):
    """

    :param Kent: Dataframe
    :param NCC: Dataframe
    :param Sussex: Dataframe
    :param column: column name either 'merchants' or 'revenue'
    :param restrictions: Dataframe of restrictions
    :return: None
    """
    K_r, = plt.plot(Kent['date'], Kent[str(column)+'_all']*100)
    NC_r, = plt.plot(NCC['date'], NCC[str(column)+'_all']*100)
    S_r, = plt.plot(Sussex['date'], Sussex[str(column)+'_all']*100)
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.legend([K_r, NC_r, S_r], ['Kent County', 'New Castle County', 'Sussex'], bbox_to_anchor=(1, 1), loc='upper left')

    restrict_line = []
    val = 1
    for i in range(len(restrictions[0])):
        if restrictions[1][i] > 1:
            mark = [str(x) for x in range(val, val + restrictions[1][i])]
            str_val = ", ".join(mark)
            val += restrictions[1][i]
        else:
            str_val = str(val)
            val += 1
        line = (pd.to_datetime(restrictions[0][i]), str_val)
        restrict_line.append(line)

    ax = plt.gca()

    for date, label in restrict_line:
        plt.axvline(x=date, color='grey', linestyle='--')
        plt.text(date, 12, label,
                 fontsize=7,
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation=90,
                 color='grey')
    plt.show()

restrictions = get_restrictions()

#de_merch, de_rev = get_state_data()
#graph_state_data(de_merch, de_rev)

Kent_m, NCC_m, Sussex_m = get_county_merch()
graph_county(Kent_m, NCC_m, Sussex_m, 'merchants', restrictions)

#Kent_r, NCC_r, Sussex_r = get_county_rev()
#graph_county(Kent_r, NCC_r, Sussex_r, 'revenue', restrictions)




