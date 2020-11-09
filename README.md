# File server

This file server is used to upload and download files using `REST APIs`

  - `POST` - upload a file
  - `GET` - to retrieve a file

### Requirements

- `Python: 3.9+`
- `Django: 3.1+`
- `Postgres 12+`
- `Redis 6+`
- `gettext package`
- `pipenv module`

### Environment variables

Copy `local.example.env` from `/file_server/settings` to `file_server/settings/local.env` and edit it using `vim`. This file contains all the local variables that `File server` needs to run including database credentials, URLs and tokens to external APIs and etc. 

- `cp file_server/settings/local.example.env file_server/settings/local.env`

- Edit `local.env` to match environment variables:

```shell
set -a
. ./file_server/settings/local.env
set +a
```

- If you're using `uWSGI` and `systemd` to run `File server` make sure to source environment file before `ExecStart` using `EnvironmentFile=/path/to/fileserver/file_server/settings/local.env`  


### Install python modules

Use these commands to install `python` and required modules automatically:

- `pipenv install`

The project virtual environment can be activated with:

- `pipenv shell`

### Database migrations

- `python manage.py makemigrations`
- `python manage.py migrate`

### Caching

`File server` uses `redis` to cache file and owners. make sure `redis` is installed and running

### Static files

Copy all static file from all folders to base folder using ` collectstatic` command.

- `python manage.py collectstatic`

### Translations

To compile translated messages you can use django's `complemessages` command:

- `python manage.py compilemessages`

### Super user

To create a super user use `createsuperuser` command:

- `python manage.py createsuperuser`

### Docker mode

Go to `docker` directory and run `docker-compose up -d`:

- To install run `docker-compose exec file_server_app_1 docker/commands/install.sh` 
- To update run `docker-compose exec file_server_app_1 docker/commands/update.sh` 

### Usage

File server uses `API Key` to handle authentication and authorization, each user should have an `API Key` and use it in `HTTP_Authorization` with this format:

`ApiKey-Files API_KEY`. e.g.:

- `curl -F file=@/home/file.zip http://fileserver.example/api/v1/files/ -H "Authorization: ApiKey-Files 5440d70ba9044e8a983d1f30e68fa031"`

#### Usage examples for python:

1. Get files:

```shell
import requests

url = "http://127.0.0.1:9596/api/v1/files/"

payload = ""
headers = {'authorization': 'ApiKey-Files a55ac299eadc445e91f139758ad44ce0'}

response = requests.request("GET", url, data=payload, headers=headers)
```

2. Upload files:

```shell
import requests

url = "http://127.0.0.1:9596/api/v1/files/"

payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"file\"\r\n\r\n\r\n-----011000010111000001101001--\r\n"
headers = {
    'authorization': "ApiKey-Files 5440d70ba9044e8a983d1f30e68fa031",
    'content-type': "multipart/form-data; boundary=---011000010111000001101001"
    }

response = requests.request("POST", url, data=payload, headers=headers)
```

3. Delete a file:

```shell
import requests

url = "http://127.0.0.1:9596/api/v1/files/5e740209-0dde-483a-b542-bf1ea153446b/"

payload = ""
headers = {
    'authorization': "ApiKey-Files 5440d70ba9044e8a983d1f30e68fa031",
}

response = requests.request("DELETE", url, data=payload, headers=headers)

print(response.text)
```

4. Download a file:

```shell
import requests

url = "http://127.0.0.1:9596/api/v1/files/d46db92a-8a84-4ae5-a39f-44e810dcfa62/"

payload = ""
headers = {'authorization': 'ApiKey-Files 5440d70ba9044e8a983d1f30e68fa031'}

response = requests.request("GET", url, data=payload, headers=headers)
```
