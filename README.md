# Ticket Store

This is a quick implementation of a reusable Django app built on Django REST Framework.  It demonstrates dynamic fields and

### Prerequisites

A correctly installed Docker / Docker Compose environment.

## Getting Started

Once you have docker set up, navigate into the root directory with the docker-compose.yml file and run:

docker-compose up

Make sure you aren't using 0.0.0.0:8000, or it will fail.

## Testing and Linting

To run the tests, start the docker container, and run the following:

docker exec -it ticket-store_app_1 python3 manage.py test

To run the linters, start the docker container and run the following:
docker exec -it ticket-store_app_1 pylint ticket-store