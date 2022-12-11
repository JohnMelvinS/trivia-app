# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

- API Versioning
    - https://stackoverflow.com/a/28797512
    - https://flask.palletsprojects.com/en/2.2.x/blueprints/

1. Use Flask-CORS to enable cross-domain requests and set response headers.

## API Documentation

### Getting Started
- Base URL: At present this backend app can only be run locally and is not hosted as a base URL. It is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity

### Endpoints

`GET '/api/v1/categories'`

- Returns a list of `categories` objects and `success` value
- Request Parameters: None
- Sample: `curl "http://127.0.0.1:5000/api/v1/categories"`

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

`GET '/api/v1/questions'`

- Returns a list of `questions` objects, `categories` objects, `current_category`, `total_questions` and `success` value
- Request Parameters:
    - `page`: Results are paginated starting from 1.
- Sample: `curl "http://127.0.0.1:5000/questions?page=2"`

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

`DELETE '/api/v1/questions/{id}'`

- Returns `success` value
- Request Parameters: None
- Sample: `curl -X DELETE "http://127.0.0.1:5000/api/v1/questions/19"`

```json
{
  "success": true
}
```

`POST '/api/v1/questions' - Create`

- Returns `success` value
- Request Parameters: None
- Request Body:
    - `question`
    - `answer`
    - `category`
    - `difficulty`
- Sample: `curl "http://127.0.0.1:5000/api/v1/questions" -X POST -H "Content-Type: application/json" -d '{"question":"Who discovered penicillin?", "answer": "Alexander Fleming","category" :"1", "difficulty":"3"}'`

```json
{
  "success": true
}
```

`POST '/api/v1/questions' - Search`

- Returns a list of `questions` objects, `current_category`, `total_questions` and `success` value
- Request Parameters: None
- Request Body:
    - `searchTerm`
- Sample: `curl "http://127.0.0.1:5000/api/v1/questions" -X POST -H "Content-Type: application/json" -d '{"searchTerm":"World Cup"}'`

```json
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

`GET '/api/v1/categories/{id}/questions'`

- Returns a list of `questions` objects, `current_category`, `total_questions` and `success` value
- Request Parameters:
    - `page`: Results are paginated starting from 1.
- Sample: `curl "http://127.0.0.1:5000/api/v1/categories/1/questions"`

```json
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 29, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

`POST '/api/v1/quizzes'`

- Returns `success` value
- Request Parameters: None
- Request Body:
    - `quiz_category`
    - `previous_questions`
- Sample: `curl "http://127.0.0.1:5000/api/v1/quizzes" -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Sports","id":"6"}, "previous_questions":[10]}'`

```json
{
  "question": {
    "answer": "Uruguay", 
    "category": 6, 
    "difficulty": 4, 
    "id": 11, 
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }, 
  "success": true
}
```

## Unit Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
