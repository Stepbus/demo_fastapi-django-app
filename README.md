# FastAPI Django App

A simple application using Django and FastAPI. 
A Django application is mounted inside a FastAPI application, which allows you to:
#### ● Use Django Admin; 
#### ● Use a faster API with FastAPI; 
#### ● Enjoy all the benefits of Django ORM without the hassle. 

## Feature
* **Python** 3.12+
* [Poetry](#https://python-poetry.org/) for dependency management
* **Docker-ready** (see [here](#docker))
* **PostgreSQL**
* **PGAdmin** for database management and convenient table browsing outside the Django admin panel
* **Redis** for Celery tasks
* **Celery** for running periodic tasks

## Installation
To create a new project, you need to:

### Clone repository 
```bash
git clone git@github.com:Stepbus/demo_fastapi-django-app.git
```

### Go into the project directory
```bash
cd demo_fastapi-django-app
```

### Make an .env file from the .dist.env file and add the necessary values
```bash
cp .dist.env .env
```

### Docker
The project includes Dockerfiles and docker-compose configuration for running application in containers.

To manage project, you need to build a docker container, for this:
```bash
docker compose up -d --build
```
Create superuser:
```bash
docker compose exec fastapi-django python /app/src/manage.py createsuperuser
```

## Usage

### endpoints
```aiignore
http://0.0.0.0:8000/docs
```
This is SWAGGER documentation
* Authorization is required.
* You can use the superuser you created earlier or create a new one. 
* The user status **is_active** by default.
* The jwt token (access and refresh) is used.
* Endpoint `/api/v1/auth/me` - only for checking the authorization service, returns the current user

```aiignore
http://0.0.0.0:8000/django/admin/
```
This is django admin panel endpoints.
* Periodic tasks do not run automatically to allow you to control the process.
* It is also convenient to run tasks through the admin panel.
* CoinMarketCap requires an API key, which I do not have, but you can add your own key to the database.
The key is checked automatically, so we can create both tasks!

#### Endpoints:
```aiignore
https://api.blockchair.com/ethereum/stats - ETH BLOCKCHAIR
https://pro-api.coinmarketcap.com/v1/blockchain/statistics/latest - BTC COINMARKETCAP
```
After logging in to the admin panel, go to the **"Periodic tasks"** table in the **"PERIODIC TASKS"** section.

Create a task for btc.
* Select “Add periodic task” at the top right.
* Add a Name (any).
* Select in the _“Task (registered):”_ field - "_**fetch_btc_block**_" task.
* Select the _“Interval Schedule:”_ field. Set the _“Number of Periods:”_ field to _**1**_.
* Set the _“Interval Period:”_ to _**“Minutes”**_

Create a task for eth. 
* The same as for btc, just choose a new name and select a task for eth - **_"fetch_eth_block"_**.

#### The results will appear within a minute. 
#### Please note that “Blocks” will be filled with data only for ETH BLOCKCHAIR until you add your api key for COINMARKETCAP