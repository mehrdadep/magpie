# File server

This file server is used to upload and download files using `REST APIs`

  - `POST` - upload a file
  - `GET` - to retrieve a file

### Requirements
- `Python: 3.7.5`
- `Django: 3.0.2`
- `Postgres 11.5`
- `Memcached 1.5.10`
- `gettext package`


### Installation
- `pipenv install`
- `pipenv shell`
- `python manage.py runserver`

### Usage
File server uses `API key` to handle authentication and authorization, each user should have a `API key` and use it in `HTTP_Authorization` with this format:
`ApiKey-Files API_KEY`. e.g.:
- `curl -F file=@/home/file.zip http://fileserver.example/api/v1/files/ -H "Authorization: ApiKey-Files 5440d70ba9044e8a983d1f30e68fa031"`
