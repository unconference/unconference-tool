## Install

Ensure `pipenv` is installed see https://docs.pipenv.org/ for how to setup on your platform of choice.

To get started and set-up virtualenv and install dependencies initially:
```
git clone https://github.com/unconference/unconference-tool/
cd unconference-tool
pipenv install --dev
```

To run locally (and set-up development DB (`dev.db`)/apply migrations):
```
pipenv shell
flask db upgrade
flask run
```
Remember you should probably also run `flask db upgrade` after pulling updates. And when messing with the DB Schema remember to build migrations (`flask db migrate`), unfortunately these should probably also be checked due to the limitations with Alembic in tracking changes see [here](http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect) for details.

N.b this assumes that the development environment variables have been set appropriately by `flask run` from the `.flaskenv` file. Else you will need to set these:
```
export FLASK_APP=app.py
export FLASK_ENV=development
```