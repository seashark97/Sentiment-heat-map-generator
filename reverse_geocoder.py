import json
from matplotlib.path import Path

def reverse_geocode(tweet):
	# print index
	# latlong = json.load(tweets)[index]['coordinates']
	latlong = tweet["coordinates"]
	if latlong == [0.0, 0.0]:
		return False
	# latlong.reverse()
	with open('world-countries.json.txt', 'r') as countries_json:
		found_country = None
		countries = json.load(countries_json)['features']
		for country in countries:
			country_name = country['properties']['name']
			if country['geometry']['type'] == 'Polygon':
				country_vertices = country['geometry']['coordinates'][0]
				country_path = Path(country_vertices)
				if country_path.contains_point(latlong):
					found_country = country_name
					break
			if country['geometry']['type'] == 'MultiPolygon':
				country_polygons = country['geometry']['coordinates']
				for polygon in country_polygons:
					country_vertices = polygon[0]
					country_path = Path(country_vertices)
					if country_path.contains_point(latlong):
						found_country = country_name
						break
		if not found_country:
			found_country = False
	return found_country
# with open('Ferguson_tweets.txt', 'r') as tweets:
# 	print reverse_geocode(tweets, 0)