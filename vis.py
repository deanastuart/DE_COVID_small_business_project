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
    con = connect_sql()
    de_merch = pd.read_sql('select date, merchants_all from state_merch where statefips = 10;',con)
    de_rev = pd.read_sql('select date, revenue_all from state_rev where statefips = 10', con)
    return de_merch, de_rev

def get_county_merch():
    con = connect_sql()
    Kent_m = pd.read_sql('select date, merchants_all from county_merch where countyfips = 10001;', con)
    NCC_m = pd.read_sql('select date, merchants_all from county_merch where countyfips = 10003;', con)
    Sussex_m = pd.read_sql('select date, merchants_all from county_merch where countyfips = 10005;', con)
    return Kent_m, NCC_m, Sussex_m

def get_county_rev():
    con = connect_sql()
    Kent_r = pd.read_sql('select date, revenue_all from county_rev where countyfips = 10001;', con)
    NCC_r = pd.read_sql('select date, revenue_all from county_rev where countyfips = 10003;', con)
    Sussex_r = pd.read_sql('select date, revenue_all from county_rev where countyfips = 10005;', con)
    return Kent_r, NCC_r, Sussex_r

def get_restrictions():
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
    merch, = plt.plot(df1['date'], df1['merchants_all']* 100)
    rev, = plt.plot(df2['date'], df2['revenue_all'] * 100)
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.legend([merch, rev], ['Merchant', 'Revenue'])
    plt.show()

def graph_county_merch(Kent, NCC, Sussex):
    K, = plt.plot(Kent['date'], Kent['merchants_all']*100, label='Kent County')
    NC, = plt.plot(NCC['date'], NCC['merchants_all']*100, label='New Castle County')
    S, = plt.plot(Sussex['date'], Sussex['merchants_all']*100, label='Sussex')
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.legend([K, NC, S], ['Kent County', 'New Castle County', 'Sussex'])
    plt.show()

def graph_county(Kent, NCC, Sussex, column, restrictions):
    K_r, = plt.plot(Kent['date'], Kent[column]*100)
    NC_r, = plt.plot(NCC['date'], NCC[column]*100)
    S_r, = plt.plot(Sussex['date'], Sussex[column]*100)
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

    """    
    restrict = [
        (pd.to_datetime("2020-03-12"), '1'),
        (pd.to_datetime("2020-03-22"), '2'),
        (pd.to_datetime("2020-03-29"), '3'),
        (pd.to_datetime("2020-04-24"), '4'),
        (pd.to_datetime("2020-04-28"), '5'),
        (pd.to_datetime("2020-05-08"), '6'),
        (pd.to_datetime("2020-05-12"), '7'),
        (pd.to_datetime("2020-05-22"), '8, 9'),
        (pd.to_datetime("2020-06-01"), '10, 11'),
        (pd.to_datetime("2020-06-15"), '12'),
        (pd.to_datetime("2020-06-20"), '13'),
        (pd.to_datetime("2020-06-22"), '14')
    ]
    """
    ax = plt.gca()

    for date, label in restrict_line:
        plt.axvline(x=date, color='grey', linestyle='--')
        plt.text(date, 12, label,
                 fontsize=7,
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation=90,
                 color='grey')

    #datacursor(K_r)
    plt.show()
"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(Kent['revenue_all'], cmap=cm.jet, interpolation='nearest')

    numrows, numcols = X.shape

    def format_coord(x, y):
        col = int(x + 0.5)
        row = int(y + 0.5)
        if col >= 0 and col < numcols and row >= 0 and row < numrows:
            z = X[row, col]
            return 'x=%1.4f, y=%1.4f, z=%1.4f' % (x, y, z)
        else:
            return 'x=%1.4f, y=%1.4f' % (x, y)

    ax.format_coord = format_coord
"""

restrictions = get_restrictions()

#de_merch, de_rev = get_state_data()
#graph_state_data(de_merch, de_rev)

Kent_m, NCC_m, Sussex_m = get_county_merch()
graph_county(Kent_m, NCC_m, Sussex_m, 'merchants_all', restrictions)

#Kent_r, NCC_r, Sussex_r = get_county_rev()
#graph_county(Kent_r, NCC_r, Sussex_r, 'revenue_all', restrictions)




