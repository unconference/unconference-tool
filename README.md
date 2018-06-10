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
Remember you should probably also run `flask db upgrade` after pulling updates. And when messing with the DB Schema remember to build migrations (`flask db migrate`), unfortunately these should probably also be checked due to the limitations with Alembic in tracking changes see [here](http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect) for details.

N.b this assumes that the development environment variables have been set appropriately by `pipenv` from the `.flaskenv` file. Else you will need to set these:
```
export FLASK_APP=app.py
export FLASK_ENV=development
```