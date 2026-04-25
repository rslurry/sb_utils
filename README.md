## depot: a Python library of map-making utilities for Subway Builder

## Requirements
This library is confirmed to work with the following Python package versions:
| Package            | Version       |
| ------------------ |:-------------:|
| python             | 3.13.9        |
| duckdb             | 1.5.1         |
| geopandas          | 1.1.1         |
| mapbox_vector_tile | 2.2.0         |
| numpy              | 2.3.5         |
| pandas             | 2.3.3         |
| shapely            | 2.1.2         |
| duckdb             | 1.5.1         |

You can prepare a [conda](https://docs.conda.io/projects/conda/en/stable/index.html) 
environment with these package versions using the supplied environment file:

    conda env create -f environment.yml

If you don't already have a preferred Python environment manager, I suggest 
using conda.  At the link above, download the Miniforge installer for your OS. 
Run it and follow the instructions.  Then you can use the above command to 
replicate the environment that is confirmed to work for this library.

In addition to the Python environment, all of the following CLI programs must be 
available within your path to create the non-demand files needed for custom maps:
* node
* [mapshaper](https://github.com/mbloch/mapshaper)
* [osmium](https://osmcode.org/osmium-tool/)
* java
* [tippecanoe and tile-join](https://github.com/felt/tippecanoe)
* sqlite3
* jq
* [pmtiles](https://github.com/protomaps/go-pmtiles/releases)
* [planetiler.jar](https://github.com/onthegomap/planetiler/releases)

These must be executable (even `planetiler.jar` despite that .jar files are not executable) 
so that `depot` can determine that they are available.  The code will not run if any of 
these requirements are missing.

## Installation
In the repo directory, run

    pip install .

## Usage

At present, `depot` includes the ability to create the non-demand files for 
custom maps.  This is handled through the `MapGen` class.

### `MapGen` inputs
| Parameter            | Description       |
| ------------------ |:-------------:|
| `city`             | str. 2-4 character city code.        |
| `bbox`             | list of floats. Bounding box for the map. [min_lon, min_lat, max_lon, max_lat]         |
| `osmpbf`          | str. Path to local .osm.pbf file to use as a source. Obtain it from <https://download.geofabrik.de/>        |
| `outputdir` | str. Path to output directory. Within the specified directory, a new directory named `city` will be created to hold all outputs and intermediate files. Defaults to the current directory. Default: current working directory         |
| `building_index_filter_size`              | int. Filters buildings below this size (in m^2) for collisions. Default: 40         |
| `building_tile_filter_size`               | int. Filters buildings below this size (in m^2) for pmtiles. Must be <= `building_index_filter_size`.  If None, it is set to `building_index_filter_size`. Default: None         |
| `cities`             | list of str. OSM 'place' values to show at the lowest zooms. If None, labels will not be created for that zoom. Default: None         |
| `suburbs`             | list of str. Like cities, but for medium zooms. Default: None         |
| `neighborhoods`             | list of str. Like cities, but for the highest zooms. Default: None         |
| `buildings_geojson`                | str or None. If a string, path to a buildings.geojson file to use as input. If None, fetches Overture buildings. Default: None |
| `redownload_buildings`             | bool. Determines whether to re-fetch buildings (True) or load previously-saved buildings if available (False). Default: False        |
| `ncores`             | int. Number of cores to use when processing tiles in parallel. Setting this to None will use all available cores. Default: 1         |
| `cleanup_files`             | bool. If True, deletes some intermediate files that are created and used within the same function. Default: True         |
| `RAM`             | int or float. Sets the amount of RAM in GB to use when calling mapshaper.  If you get heap allocation errors, increase this value.  Keep in mind your OS and other programs still need to run, so don't try to allocate your system's full RAM amount. Default: 4         |
| `verb`             | bool. Determines whether to print additional info or not. Default: True        |

### `MapGen` methods that you care about
| Class method                 | Description                                                    |
| ---------------------------- |:--------------------------------------------------------------:|
| `extract_base_data`          | osmium extract for base layers                                 |
| `process_buildings`          | Fetch Overture buildings and create buildings_index.json       |
| `process_roads_and_aeroways` | Creates roads.geojson and runways_taxiways.geojson             |
| `generate_pmtiles`           | Creates the PMTiles file with no labels                        |
| `add_labels`                 | Adds labels to the PMTiles file created by `generate_pmtiles`  |
| `run_all`                    | Runs the above 5 methods consecutively                         |

These methods take no inputs; they use what you provide when initializing the 
object. `extract_base_data` must be executed first; `process_buildings` must be executed before `generate_pmtiles`; 
and `generate_pmtiles` must be executed before `add_labels`.

You may need to re-run `generate_pmtiles` multiple times to ensure that there 
aren't tile size issues at certain zooms; you will see a warning message if 
there is that will mention the file size (e.g., 591365) exceeds the maximum 
allowed size (500000).  Adjust the relevant limit (e.g., `z12_limit` for issues 
with tiles at zoom 12) and re-run until you do not have any of those messages.

You may also want to re-run `add_labels` multiple times to decide which place 
tags should be in which categories.

### Labels
You may want to look at OSM's list of available 'place' keys: <https://wiki.openstreetmap.org/wiki/Key:place>

For the maps I have made, here are the setups I chose:

    US maps:
        cities = ['city', 'borough', 'town']
        suburbs = ['suburb', 'village']
        neighborhoods = ['neighbourhood', 'hamlet', 'quarter', 'locality']
    PR maps:
        cities = ['city', 'borough', 'town']
        suburbs = ['suburb']
        neighborhoods = ['village', 'quarter']
    MX maps:
        cities = ['city', 'borough']
        suburbs = ['city', 'borough', 'town', 'suburb']
        neighborhoods = ['city', 'borough', 'town', 'suburb', 'village', 'hamlet']

## Future plans
At some point I will add a way to create and manipulate demand data.  Stay tuned.

## Contributions
I'd love for people to continue developing this tool so that it can serve the needs of the community. 
Feel free to submit Pull Requests with new features, optimizations, etc.

## Questions?  Issues?  Requests?

Open an issue here on GitHub or provide feedback in Discord.

## License

This library is made available under the GPL v3 license.  See LICENSE for details.
