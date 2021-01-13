import folium
import os
import json
import pandas as pd

#create map object
m = folium.Map(location = [39.1582,-75.5244], zoom_start=9)

# make tooltip
tooltip = 'Click for More Info'

# #create custom marker icon
# logoIcon = folium.features.CustomIcon("/Users/luke/Downloads/covid-19.jpg", icon_size=(50,50))

#create Vega data
vis = os.path.join("/Users/luke/Final_Project_2/data/vis.json")

#bring in zip codes

overlay = os.path.join("/Users/luke/Final_Project_2/data/de_delaware_zip_codes_geo.min.json")


file_path = '/Users/luke/Final_Project_2/data/markers.json'
with open(file_path, 'r') as f:
    zipcode_central = json.load(f)

#Creates all markers
for key, item in zipcode_central.items():
    folium.Marker(item,
              #pops up when clicked
              popup = f'<strong>{key}</strong>',
              #hover over it says "message"
              tooltip=tooltip).add_to(m)




# #custom image marker
# folium.Marker([42.36500,-71.097500],
#               #pops up when clicked
#               popup = '<strong>Location Two</strong>',
#               #hover over it says "message"
#               tooltip=tooltip,
#               icon = logoIcon).add_to(m),
#
# folium.Marker([42.315140,-71.072450],
#               #pops up when clicked
#               popup = folium.Popup(max_width=450).add_child(folium.Vega(json.load(open(vis))))).add_to(m)

#geojson overlay

folium.GeoJson(overlay,name = "DE_ZipCodes").add_to(m)



#generate map
m.save('map.html')