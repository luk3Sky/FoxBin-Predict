# FoxBin-Predict
Real time websocket server for ml predictions

## Install
* Install Python 3.6+
* Install pipenv or virtualenv to the Python system, if not already done

*linux/ubuntu*
```
$ pip3 install virtualenv
```
#### or
*windows*
```
$ python -m pip install virtualenv 
```
* Create virtual environment for this project and install dependencies
```
$ py -m venv env
```
* Install dependencies
```
$ python -m pip install -r requirements.txt
```

## Run

```
$ python manage.py runserver
```

Websocket is listening on: <ws://localhost:8000/>

## Test

```
python manage.py test
```
