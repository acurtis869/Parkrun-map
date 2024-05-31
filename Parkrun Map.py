import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium

# Load borough boundaries
boroughs = gpd.read_file("Shape Files/London_Borough_Excluding_MHW.shp")

# Load facilities data
facilities = pd.read_csv("London Facilities.csv").dropna()
facilities_gdf = gpd.GeoDataFrame(
    facilities, geometry=gpd.points_from_xy(facilities.longitude, facilities.latitude))

# Plot static map
#fig, ax = plt.subplots(figsize=(10, 10))
#boroughs.plot(ax=ax, edgecolor='black')
#facilities_gdf.plot(ax=ax, color='red', markersize=10)
#plt.title("London Borough Boundaries with Facilities")
#plt.show()

# Create interactive map
m = folium.Map(location=[51.495204, -0.183746], zoom_start=14)

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

# Add facilities to the map
for idx, row in facilities.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['Centre Name']).add_to(m)

# Add Cromwell Road
latitude = 51.495204
longitude = -0.183746
label = "100 Cromwell Road"

folium.Marker(
    location = [latitude, longitude],
    icon = folium.Icon(color = 'red'),
    popup = label
).add_to(m)

# Save the map to an HTML file
m.save("cromwell_road_map.html")