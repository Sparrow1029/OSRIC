# D&D Database
### A character / player/ campaign management application for AD&D 1st Edition (OSRIC)
-------
## The application consists of:
- Mongodb backend interface using _Flask_, _Flask-mongoengine_
- REST API with _Flask-restx_
- Front-end web-application created with _React_

## Deploy locally:
-------
#### Requirements:
- mongodb needs to be installed and running locally (default 127.0.0.1 port 27017)
- Python3.6+ (everything here was made using Python3.8)

#### Notes:
- The `client` (React application) does not work right now
- I recommend installing [MongoDB Compass](https://www.mongodb.com/try/download/compass) (community edition works fine) for interactive visibility into the mongo database

Steps to deploy current iteration:
1. clone the repo `git clone https://github.com/Sparrow1029/OSRIC.git`
2. create a virtualenv using virtualenv or virtualenvwrapper: ```bash
$ cd OSRIC/
$ virtualenv venv/
$ . venv/bin/activate
$ pip install -r requirements.txt```
3. Seed the database: ```bash
$ cd api/
$ python manage.py```
4. create a `.env` file in the `api/` directory with the contents: `JWT_SECRET_KEY="some-super-secret-key"`
5. export some other flask shell variables: ```bash
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=1
$ export ENV_FILE_LOCATION=.env
```
6. Run the API with `flask run`
7. Navigate to http://localhost:5000/ to see the Swagger doc/api
8. Use `mongo` CLI or MongoDB Compass to view database
