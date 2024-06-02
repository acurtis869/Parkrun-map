import geopandas as gpd
import pandas as pd
import folium
import branca.colormap as cm

# Load borough boundaries
boroughs = gpd.read_file("Shape Files/London_Borough_Excluding_MHW.shp")

# Load parkruns data
parkruns = pd.read_csv("Parkruns.csv")
parkruns_gdf = gpd.GeoDataFrame(
    parkruns, geometry=gpd.points_from_xy(parkruns.Longitude, parkruns.Latitude))

# Calculate the percentage of completed parkruns for each borough
borough_completion = parkruns.groupby('Borough')['Completed'].value_counts(normalize=True).unstack(fill_value=0)
borough_completion['Percentage'] = borough_completion.get('Yes', 0) * 100

# Merge with the boroughs GeoDataFrame
boroughs = boroughs.merge(borough_completion['Percentage'], left_on='NAME', right_index=True, how='left')

# Replace NaN values in the 'Percentage' column with 'No Parkruns'
boroughs['Percentage'] = boroughs['Percentage'].fillna(100)

# Create a color map
colormap = cm.LinearColormap(colors=['red', 'yellow', 'green'], vmin=0, vmax=100)
colormap.caption = 'Percentage of Parkruns Completed'

# Create interactive map
m = folium.Map(location=[51.475031657317174, -0.1225806048841719], zoom_start=11)

# Define the style function to customize borders and remove fill
def style_function(feature):
    percentage = feature['properties']['Percentage']
    return {
        'fillColor': colormap(percentage),
        'color': 'black',            # Border color
        'weight': 2,                 # Border thickness
        'fillOpacity': 0.3             # Fill opacity
    }

# Create a formatted percentage column
boroughs['Formatted_Percentage'] = boroughs['Percentage'].apply(lambda x: f"{x:.1f}%")

# Add borough boundaries to the map with custom style
folium.GeoJson(boroughs, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['NAME', 'Formatted_Percentage'], aliases=['Borough:', 'Completed Percentage:'])).add_to(m)

# Add parkruns to the map
for idx, row in parkruns.iterrows():
    if row['Completed'] == 'Yes':
        popup_content = f"{row['Parkrun']}<br>PB: {row['Time']}"
        color = 'green'
    else:
        popup_content = row['Parkrun']
        color = 'red'
    
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        popup=popup_content,
        icon=folium.Icon(color=color)
    ).add_to(m)

# Add colormap to the map
colormap.add_to(m)

# Calculate completed parkruns statistics
total_parkruns = len(parkruns)
completed_parkruns = parkruns[parkruns['Completed'] == 'Yes'].shape[0]
completion_percentage = (completed_parkruns / total_parkruns) * 100

# Add text to the top right of the HTML page
html = f"""
<div style="position: absolute; bottom: 15px; right: 10px; background-color: white; padding: 10px; z-index: 9999;">
    London Parkruns Completed: {completed_parkruns} out of {total_parkruns} ({completion_percentage:.1f}%)
</div>
"""
m.get_root().html.add_child(folium.Element(html))


# Save the map to an HTML file
m.save("parkrun_map.html")