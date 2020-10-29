# Revercipe 

## Begin
* Clone repo 
```
git clone https://github.com/ChicoState/Revercipe.git
```
* Go into the repo
```
cd Revercipe
```
* Run Docker
```
docker-compose up
```

## Help
* Get into container's shell
```
docker-compose run web /bin/bash
```

* Migrate database
```
python manage.py makemigrations
python manage.py migrate
```

## Regular files
* **Dockerfile** - Initial dockerfile to help us setup our environment
* **docker-compose.yml** - Initial starter docker-compose file
* **requirements.txt** - Blank requirements.txt file for us to add python package requirements into

## Hidden files
* **.gitignore** - ignores python code & macOS generated files that don't need to be in the repo

## Techs used 
Click for documentation.
* [Django](https://docs.djangoproject.com/en/2.2/)
* [Docker](https://docs.docker.com/engine/docker-overview/)
* [Foundation](https://foundation.zurb.com/sites/docs/)

[![Build Status](https://travis-ci.com/txiong11/Revercipe.svg?branch=master)](https://travis-ci.com/txiong11/Revercipe)
