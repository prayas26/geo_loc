from gmplot import gmplot
import googlemaps

locations = [
	['Cronulla Beach', -34.028249, 151.157507, 3],
	['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
	['Maroubra Beach', -33.950198, 151.259302, 1],
	['adhoc', 26.8487734, 75.7982246, 6],
	['indore', 22.7241158, 75.79381, 7]
]

gmaps = googlemaps.Client(key="AIzaSyCEA9EJC94BKr4RH_7OTPHf_yJLBR-8ivg")
loc = gmaps.geolocate()
pre_lat = loc['location']['lat']
pre_lng = loc['location']['lng']

# Place map
gmap = gmplot.GoogleMapPlotter(pre_lat, pre_lng, 7)
# gmap.heatmap(golden_gate_park_lats, golden_gate_park_lons)

# Marker
# hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
for each in locations:
    gmap.marker(each[1], each[2], color='black', title=each[0])

# Draw
gmap.draw("my_map.html")