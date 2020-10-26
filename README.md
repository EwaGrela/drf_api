# Description
1. drf_api project was created
2. drf_api contains cars app 
3. project and app are written in Django Rest Framework 
4. project is dockerized; in drf_api folder a Dockerfile and docker-compose.yml files exist.
To run application locally, enter project directory (containing these files) and run:

```
cd drf_api
sudo docker-compose build
sudo docker-compose up
```
Open app on: http://127.0.0.1:8000/cars or http://0.0.0.0:8000/cars
If one opens at http://127.0.0.1:8000, they will be redirected to /cars page

5. The app contains several endpoints:

### `/cars`
* **GET, POST**
    GET:
    a list of available cars with all the data - average rating, number of times a car was rated, etc
    POST:
    enpoint where user posts data in json format, with make and model of a car:

    ```json
        {
            "make": "honda",
            "model": "Civic"
        }
    ```
    a module get_external_data() from helpers.py checks if such car exists in external API, if so it is saved in our database
    if not - user is informed such car does not exist (error 404)
    module validate_car_data() checks for posted data validity
    if user sends data in wrong format, they receive bad request (error 400)

    Important: Car make is case insensitive:
    if one sends car make in uppercase and such model is found, it is saved to DB in uppercase. Model names in external API are in uppercase;
    if one sends car make in lowercase, model will be also found in external API and car make will we saved in uppercase, because make names in external DB are in uppercase

### `/rate`
* **POST**
    POST:
    data is send in json format, containing make name, model name and its rate; such car is found in database and its rating updated
    ```json
        {   "make": "honda",
            "model": "Civic",
            "score": 3
        }
    ```
    Validations are performed: 
    if car exists in DB (error 404)
    if data is in proper format (error 400)
    Rating is case insensitive, one can sends json with car make in uppercase or lowercase, they will rate the same car.

### `/popular`
* **GET**
    GET:
    a list of cars present in database is returned, all sorted based on their popularity - number of times they were rated (not sum of rates or average rate)

6. postgreSQL is used as database (switched from SQLite in order to persist data on heroku)

7. Tests for API are written in tests.py file, in order to run them:
```bash
    cd drf_api
    sudo docker-compose run web python manage.py test 
```
8. File requirements.txt contains requirements necessary to run app and create virtual environment.
    To create virtual environment do the following:

```bash
      pip install venv
      source venv/bin/activate
      pip install -r requirements.txt
```
9.  In order to autoformat code activate virtual environment (step 8) and run:
```bash
     autopep8 --in-place --aggressive --aggressive *.py
```

10. API is available on heroku: [cars](https://drf-cars-api.herokuapp.com/cars/) for cars, 
     [rate](https://drf-cars-api.herokuapp.com/rate/) for rating
      [popularity](https://drf-cars-api.herokuapp.com/popular/) for popularity check



