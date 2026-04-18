import sys, os
import numpy as np
from sb_utils.maps import MapGen
import requests

# Download the .osm.pbf file we need
if not os.path.exists('california-latest.osm.pbf'):
    resp = requests.get('https://download.geofabrik.de/north-america/us/california/socal-latest.osm.pbf')
    with open('socal-latest.osm.pbf', 'wb') as f:
        f.write(resp.content)

# Set up MapGen object
obj = MapGen(city='LAXM', bbox=[-118.66816, 33.70200, -117.96758, 34.33162],
             osmpbf='socal-latest.osm.pbf',
             building_filter_size=180, z13_limit=200, z12_limit=200, ncores=16,
             RAM=12, 
             cities = ['city', 'borough', 'town'],
             suburbs = ['suburb', 'village'],
             neighborhoods = ['neighbourhood', 'hamlet', 'quarter', 'locality'])

# If you want to run each method individually:
#obj.extract_base_data()
#obj.process_buildings()
#obj.process_roads_and_aeroways()
#obj.generate_pmtiles()
#obj.add_labels()

# Or just run them all consecutively:
obj.run_all()
