import folium
import pandas as pd
import os
import json

zipcodes = os.path.join("/Users/luke/Final_Project_2/data/de_delaware_zip_codes_geo.min.json")
covid_data = os.path.join("/Users/luke/Final_Project_2/covid_nums.csv")

covid = pd.read_csv(covid_data)

m = folium.Map(location = [39.1582,-75.5244], zoom_start=9)

m.choropleth(
    geo_data = zipcodes,
    name = 'Chloropleth',
    data = covid,
    columns = ['Zipcode','Value'],
    key_on = "properties.ZCTA5CE10",
    fill_color = 'YlOrRd',
    fill_opacity = 0.7,
    line_opacity = 0.2,
    legend_name = "Covid Cases (per 10,000 people)"

)

tooltip = 'Click for More Info'

file_path = '/Users/luke/Final_Project_2/data/markers.json'
with open(file_path, 'r') as f:
    zipcode_central = json.load(f)

#Creates all markers
for key, item in zipcode_central.items():
    folium.Marker(item,
              #pops up when clicked
              popup = f'<strong>Zip Code: {key}</strong><br>Number of Reported Cases: </br>',
              #hover over it says "message"
              tooltip=tooltip).add_to(m)

folium.LayerControl().add_to(m)
m.save('map2.html')