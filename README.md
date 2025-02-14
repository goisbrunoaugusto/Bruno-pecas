# Car shop management system

This a system to manage cars and parts for a car shop as a challenge for Hubbi back end developer selection

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Installation
Prerequisites:
* [Docker Installed](https://docs.docker.com/get-started/get-docker/)
* [Docker Compose Installed](https://docs.docker.com/compose/install/)
* Need a .env file inside the project folder, example below

## Usage

```bash
docker compose up --build
```
## Tests
To run tests you'll need to access the container
```bash
sudo docker exec -it <ContainerID> /bin/sh
```
The Container ID can be found by running
```bash
sudo docker ps
```

Then run the command
```bash
pytest
```

## Swagger Documentation
The Swagger documentation can be found after the project is running in the url http://localhost:8000/swagger/

## Postman Documentation
The Postman collection can be found inside the Postman folder in this project

## .env file model
POSTGRES_PASSWORD=12345\
POSTGRES_USER=bruno\
POSTGRES_DB=brunopecas\
POSTGRES_PORT=5432\
POSTGRES_HOST=db

