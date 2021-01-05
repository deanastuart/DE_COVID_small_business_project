from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


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

get_data()

