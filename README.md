# Django REST Framework Movie API

This is a simple Django REST Framework Movie API that allows users to create, read, update and delete movie records.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AliBaba05/DRF-Movie-API.git
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
6. Access the API at `http://localhost:8000/api/`.

## API Endpoints

The following endpoints are available:

### Movies

- `GET /movies`: Returns a list of all movies.
- `POST /movies`: Creates a new movie.
- `GET /movies/{id}`: Returns a single movie by id.
- `PUT /movies/{id}`: Updates a single movie by id.
- `DELETE /movies/{id}`: Deletes a single movie by id.
- `GET /movies/{id}/reviews`: Returns a list of reviews of the movie.
- `POST /movies/{id}/reviews`: Creates a new movie review for the movie.

### Directors

- `GET /directors`: Returns a list of all directors.
- `POST /directors`: Creates a new director.
- `GET /directors/{id}`: Returns a single director by id.
- `PUT /directors/{id}`: Updates a single director by id.
- `DELETE /directors/{id}`: Deletes a single director by id.

### Reviews

- `GET /reviews/{id}`: Returns a single review by id.
- `PUT /reviews/{id}`: Updates a single review by id.
- `DELETE /reviews/{id}`: Deletes a single review by id.

### MovieLists

- `GET /movielists`: Returns a list of all movielists.
- `POST /movielists`: Creates a new movielist.
- `GET /movielists/{id}`: Returns a single movielist by id.
- `PUT /movielists/{id}`: Updates a single movielist by id.
- `DELETE /movielists/{id}`: Deletes a single movielist by id.

## Authentication

This API uses Token authentication to authenticate users. To obtain a token, send a POST request to the `/auth` endpoint with your username and password:

```http
POST /auth
Content-Type: application/json

{
    "username": "your-username",
    "password": "your-password"
}
```

The server will respond with a JSON object containing your token:

```json
{
  "token": "your-token"
}
```

Include the token in subsequent requests by including the `Authorization` header with the value `Token your-token`:

```http
GET  /movies
Authorization: Token your-token
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
