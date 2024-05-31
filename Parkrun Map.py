import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium

# Load borough boundaries
boroughs = gpd.read_file("Shape Files/London_Borough_Excluding_MHW.shp")

# Load parkruns data
parkruns = pd.read_csv("Parkruns.csv")
parkruns_gdf = gpd.GeoDataFrame(
    parkruns, geometry=gpd.points_from_xy(parkruns.Longitude, parkruns.Latitude))

# Create interactive map
m = folium.Map(location=[51.475031657317174, -0.1225806048841719], zoom_start=11)

# Define the style function to customize borders and remove fill
def style_function(feature):
    return {
        'fillColor': 'transparent',  # No fill color
        'color': 'black',            # Border color
        'weight': 2,                 # Border thickness
        'fillOpacity': 0             # Fill opacity
    }

# Add borough boundaries to the map with custom style
folium.GeoJson(boroughs, style_function=style_function).add_to(m)

# Add parkruns to the map
for idx, row in parkruns.iterrows():
    color = 'green' if row['Completed'] == 'Yes' else 'red'
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        popup=row['Parkrun'],
        icon=folium.Icon(color=color)
    ).add_to(m)

# Save the map to an HTML file
m.save("parkrun_map.html")