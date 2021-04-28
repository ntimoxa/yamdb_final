# YaMDb API
YaMDb is a fictional service where users can post reviews for titles (movies and shows, music, and books) and comment on reviews. The service lets you define genres and categories for titles.
This project is a RESTful YaMDb API for interacting with the YaMDb service. The project is implemented as a multi-contaner Docker application with three services: `web` (the application itself), `db` (PostgreSQL), and `nginx` running in separate containers.
The application image is available on Docker Hub: https://hub.docker.com/r/ntimoxa/yamdb.

![yamdb_workflow](https://github.com/ntimoxa/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


## Example of Usage
- To see how it works, open http://familynetwork.ml/api/v1/


## Features
- CRUD for titles
- CRUD for reviews and comments
- CRUD for genres and categories
- Get reviews for titles
- Get comments for reviews


## Technologies
Python, Django, Nginx, Gunicorn, PostgreSQL


## Installation and use
> Make sure that you have Docker installed: https://docs.docker.com/get-started/#download-and-install-docker
1. Clone the repository: `https://github.com/ntimoxa/infra_sp2.git`
2. To start the containers, change to the project directory and run `docker-compose up`.
3. Open a new terminal and run the following:
   - Apply migrations:
     - `docker-compose exec web python manage.py makemigrations`
     - `docker-compose exec web python manage.py makemigrations api`
     - `docker-compose exec web python manage.py migrate --no-input`
   - Create a superuser: `docker-compose exec web python manage.py createsuperuser`
   - Collect static files: `docker-compose exec web python manage.py collectstatic --no-input`
4. To test that it works, open http://127.0.0.1/admin/
5. Populate the database with the initial data by running `docker-compose exec web python manage.py loaddata fixtures.json`.
To stop the containers, run `docker-compose stop`.
To remove the containers, run `docker-compose down`.
If you made any changes, run `docker-compose up -d --build` to rebuild the images and start the containers.


### Database configuration
To configure the Postgres database, Docker Compose uses the environment variables defined in the `.env` file at the project root.


## API guide
### Authorization
> For the authorization flow to work, configure your mail server settings in `settings.py`.
1. To get access to the API, make a POST request with your email address to `/api/v1/auth/email`, after which you will receive a confirmation code.
2. Submit a POST request to `/api/v1/auth/token` with your email address and the confirmation token. In response, you'll receive a JWT token.
3. When calling the API, pass the token in the header as `Authorization: Bearer [token]`.


### Example requests and responses
Sample POST request to `/api/v1/titles/2/reviews/`:
```json
{
	"text": "One of the greatest fimls I've ever seen.",
	"score": 10
}
```
Sample response:
```json
{
	"id": 2,
	"title": "The Theory of Everything",
	"author": "antony_hopkins",
	"text": "One of the greatest fimls I've ever seen.",
	"score": 10,
	"pub_date": "2021-04-08T15:21:17.556753Z"
}
```
Sample POST request to `/api/v1/titles/2/reviews/2/comments/` to add a comment to a review:
```json
{
	"text": "You're on point!",
}
```
Sample response:
```json
{
	"id": 2,
	"review": "One of the greatest fimls I've ever seen.",
	"author": "daniel_radcliffe",
	"text": "There are two heroes in the world, Harry and Steven",
	"pub_date": "2021-04-08T15:25:01.555817Z"
}
```


## Complete API reference
The full docs are available at http://127.0.0.1/redoc/ or inside the `/static` directory.


## Author
Timofey Nemchinov, a student at Yandex.Practicum Python Developer program, cohort 10.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)
