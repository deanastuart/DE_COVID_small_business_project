from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd
from sqlalchemy import create_engine
import os


def get_data():

    #save url of site being scraped to variable
    page_url = "https://myhealthycommunity.dhss.delaware.gov/locations/state/coronavirus-mitigation#contact-tracing-timeline"

    #opens the connection and downloads html page from url
    uClient = uReq(page_url)

    # parses html into a soup data structure to traverse html as if it were a json data type.
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    data = []
    #finds each element in html with "tr" tag
    containers = page_soup.findAll("tr")

    #Create csv file, with headers
    out_filename = "DE_Mitigation_Timeline.csv"
    headers = "Mitigation,Start,Until\n"

    f = open(out_filename, "w")
    f.write(headers)

    #finds each element in the table on wesbite
    count = 1
    for row in containers:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

        while count < len(data):
            Mitigation = data[count][0]
            Start = data[count][1]
            Until = data[count][2]

            count += 1

            f.write(str(Mitigation).replace(",","") + "," + str(Start) + "," + str(Until) + "\n")

    f.close()  # Close the file

def clean_data():

    df = pd.read_csv("/Users/luke/Final_Project_2/DE_COVID_small_business_project/DE_Mitigation_Timeline.csv")
    df["Start"].apply(lambda x: str(2020) + " " + x)
    df["Start"] = df["Start"].apply(lambda x: str(2020) + " " + x)
    df["Start"] = pd.to_datetime(df["Start"], format="%Y %b %d")
    df.loc[(df.Until != 'Further Notice'), 'Until'] = df["Until"].apply(lambda x: str(2020) + " " + x)
    df["Until"] = pd.to_datetime(df.loc[(df.Until != 'Further Notice'), 'Until'], format="%Y %b %d")
    df.to_csv("DE_Mitigation_Timeline.csv")

def upload_MySQL():
    #Gets MySQL password from my local machine
    mysql_connection = os.environ.get("group_sql")
    #Reads csv to a dataframe
    df = pd.read_csv("/Users/luke/Final_Project_2/DE_COVID_small_business_project/DE_Mitigation_Timeline.csv")
    #Create connection to MySQL database
    engine = create_engine(mysql_connection)

    #Drops yesterday's steam table
    connection = engine.raw_connection()
    cursor = connection.cursor()
    command = "DROP TABLE IF EXISTS {};".format('mitigation')
    cursor.execute(command)

    #uploads today's mitigation table
    df.to_sql('mitigation',con=engine, index=False)



get_data()
clean_data()
upload_MySQL()