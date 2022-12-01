# Dashboard FUSE Bhima Climate

[![latest](https://img.shields.io/github/last-commit/iiasa/CWatM_Bhima)](https://github.com/iiasa/CWatM_Bhima)
[![license](https://img.shields.io/github/license/iiasa/CWatM_Bhima?color=1)](https://github.com/iiasa/CWatM_Bhima/blob/main/LICENSE)
[![size](https://img.shields.io/github/repo-size/iiasa/CWatM_Bhima)](https://github.com/iiasa/CWatM_Bhima)

## https://fuse-bhima-climate.herokuapp.com/

## Overview 

### Fuse Bhima

is a transdisciplinary 3-year research project (2018-2021) involving the Food-Water-Energy Nexus (FWE) in Pune (India).

The project will develop a long-term systems model that can be used to identify viable paths to sustainability.
It brings together scientists, engineers, economists, and stakeholder engagement experts from

- Stanford University in California, USA
- IIASA (International Institute for Applied Systems Analysis) in Laxenburg, Austria
- UFZ (Helmholtz Centre for Environmental Research) in Leipzig, Germany
- ÖFSE (Austrian Foundation for Development Research) in Vienna, Austria

### Climate Bhima web-tool

The webtool on https://fuse-bhima-climate.herokuapp.com/ shows the climate change variability and uncertainty for the upper Bhima basin.
The tool holds the data for RCPs 4.5 and 8.5, including three General Circulation Models (GCMs) and an average of the two RCPs and three GCMs.
For different dicstricts and tehsils the change of climate variables are displayed between 1990-2020 and 2025-2055.

For temperature the change in average temperature but also the change in numbers of days with max temperature >= 38 deg C or >= 40 deg C are shown.
For precipitation the change in average precipitation and the change in numbers of days with no rain or days with heavy rain >=20mm, >=50mm, >=100mm are shown.

For a web application we are limited by the memory used to load results in time. 
Therefore the bias-corrected GCMs GFDL-ESM2M, MIROC5, MPI_REMO200 are a selection from 10 different climate model runs.

## Readme


1) create repository on https://github.com/iiasa/
    -> https://github.com/iiasa/CWatM_Bhima
	This step was already done . i have to look up how it is down
	-> result empty repository
	
2) clone repro to local disk (p-drive)
   https://github.com/iiasa/CWatM_Bhima  <>Code (green button)
   - open with Github Desktop
   URL: https://github.com/iiasa/CWatM_Bhima
   Direktory: P:/watmodel/dashboards/fuse_bhima
   
3) Init virtual environment
    cd P:\watmodel\dashboards\waterstressat_pinzgau
    git init # initializes an empty git repo
    virtualenv venv
    .\venv\Scripts\activate
    pip list

4) Installation of libraries

    - pip install plotly
    - pip install gunicorn
    - pip install xarray
    - pip install numpy
    - pip install pandas
    - pip install dash
    - pip install dash_bootstrap_components

	To create new requirement.txt:

    - pip freeze > requirements.txt
	
	
5) All the libraries in your app.py

In the directory should be:

    - app.py
    - .gitignore
    - Procfile
    - requirements.txt

6) Warm start

    cd P:\watmodel\dashboards\fuse_bhima
    virtualenv venv

7 ) Test app.py

P:/watmodel/dashboards/fuse_bhima/venv/Scripts/python app.py

8) First time deploy to heroku 

- heroku login 
- heroku create xxxxxxxxx  # change my-dash-app to a unique name -> only small letters no underscore
- git add . # add all files to git
- git commit -m 'Initial app water1'
- git push heroku main # deploy code to heroku
- heroku ps:scale web=1  # run the app with a 1 heroku "dyno"

You should be able to view your app at https://fuse-bhima-climate.herokuapp.com/

if errors:

- heroku logs --tail
- heroku logs > log1.txt

8) OR
   
- commit to iiiasa github
- Login https://dashboard.heroku.com/apps
- https://dashboard.heroku.com/apps/fuse-bhima-climate/deploy/github
- Connected to iiasa/CWatM_Bhima by CWatM CWatM


   