## Install

Ensure `pipenv` is installed see https://docs.pipenv.org/ for how to setup on your platform of choice.

To set-up virtualenv and install dependencies initially:
```
pipenv install --dev
```

To run locally:
```
pipenv shell
flask run
```

N.b this assumes that the development environment variables have been set appropriately by `pipenv` from the `.flaskenv` file. Else you will need to set these:
```
export FLASK_APP=app.py
export FLASK_ENV=development
```