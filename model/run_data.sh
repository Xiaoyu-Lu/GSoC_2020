#!/bin/bash

python3 ./data/TYY_NEWS_create_db.py --output ./data/news.npz
# Download IMDB-WIKI dataset (face only) from https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/
python3 ./data/TYY_IMDBWIKI_create_db.py --db imdb --output ./data/imdb.npz
python3 ./data/TYY_IMDBWIKI_create_db.py --db wiki --output ./data/wiki.npz
