Fuse Bhima

readme
------
PB 30/11/22

1) create reposotory on https://github.com/iiasa/
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
    ------ (pip install netCDF4)
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
