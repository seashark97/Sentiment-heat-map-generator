import vincent
import pandas as pd

world_topo = r'world-countries.topo.json'
geo_data = [{'name': 'countries',
             'url': world_topo,
             'feature': 'world-countries'}]

df = pd.read_csv('Ballon.tsv')

vis = vincent.Map(geo_data=geo_data, scale=200, data=df, data_bind='sentiment_harmonic_mean',
					data_key='country', map_key={'countries':'properties.name'}, brew='RdYlGn')
vis.to_json('map.json', html_out=True, html_path='map_example.html')