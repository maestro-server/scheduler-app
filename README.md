[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f4df72c5fbde4b59a1f7de0d9b2899dc)](https://www.codacy.com/gh/maestro-server/scheduler-app/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=maestro-server/scheduler-app&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.com/maestro-server/scheduler-app.svg?branch=master)](https://travis-ci.com/maestro-server/scheduler-app)
[![Maintainability](https://api.codeclimate.com/v1/badges/3a073f54d89d948c0c08/maintainability)](https://codeclimate.com/github/maestro-server/scheduler-app/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3a073f54d89d948c0c08/test_coverage)](https://codeclimate.com/github/maestro-server/scheduler-app/test_coverage)
[![Coverage Status](https://coveralls.io/repos/github/maestro-server/scheduler-app/badge.svg?branch=master)](https://coveralls.io/github/maestro-server/scheduler-app?branch=master)

# Maestro Server #

Maestro Server is an open source software platform for management and discovery servers, apps and system for Hybrid IT. Can manage small and large environments, be able to visualize the latest multi-cloud environment state.

### Demo ###
To test out the demo, [Demo Online](http://demo.maestroserver.io "Demo Online")

# Maestro Server - Scheduler #

Scheduler App is accountable to manage and execute internal jobs.

* Schedule jobs, interval or crontab
* Do chain jobs

----------

Scheduler use apscheduler to control scheduler jobs, `Apscheduler documentation <https://apscheduler.readthedocs.io/en/latest/>`_


![arch](http://docs.maestroserver.io/en/latest/_images/scheduler.png)

**Core API:**

* Celery Beat (Mongo Scheduler)
* Worker - Webhook
* Worker - Connections
* Worker - Chain
* Worker - Chain Exec
* Worker - Depleted Job
* Worker - Notify Event

## TechStack ##
* Python <3.6
* Celery
* RabbitMq
* MongoDB

## Connect to: ##
* Maestro Data

## Setup #

#### Installation by docker ####

```bash
version: '2'

services:
    scheduler:
        image: maestroserver/scheduler-maestro
        environment:
        - "MAESTRO_DATA_URI=http://data:5000"
        - "CELERY_BROKER_URL=amqp://rabbitmq:5672"
        - "MAESTRO_MONGO_URI=mongodb://localhost"
        - "MAESTRO_MONGO_DATABASE=maestro-client"

    scheduler:
        image: maestroserver/scheduler-maestro-celery
        environment:
        - "MAESTRO_DATA_URI=http://data:5000"
        - "CELERY_BROKER_URL=amqp://rabbitmq:5672"
        - "MAESTRO_MONGO_URI=mongodb://localhost"
        - "MAESTRO_MONGO_DATABASE=maestro-client"
```

#### Dev Env ####
```bash
cd devtools/

docker-compose up -d
```

Configure rabbitmq, data layer app in .env file

```bash
MAESTRO_DATA_URI=http://data:5000
MAESTRO_MONGO_URI=mongodb://localhost
MAESTRO_MONGO_DATABASE=maestro-client
CELERY_BROKER_URL="amqp://localhost:5672"
CELERYD_TASK_TIME_LIMIT=30
```

Install pip dependences
```bash
pip install -r requeriments.txt
```

Run beat
```bash
celery -A app.celery beat -S app.schedulers.MongoScheduler --loglevel=info

or 

npm run beat
```

Run workers
```bash
celery -A app.celery worker --loglevel=info

or 

npm run worker
```

### Env variables ###

| Env Variables                | Example                  | Description                                 |
|------------------------------|--------------------------|---------------------------------------------|
| MAESTRO_DATA_URI             | http://localhost:5010    | Data Layer API URL                          |
| MAESTRO_REPORT_URI           | http://localhost:5005    | Report App URL                              |
| MAESTRO_DISCOVERY_URI        | http://localhost:5000    | Discovery App URL                           |
| MAESTRO_ANALYTICS_URI        | http://localhost:5020    | Analytics App URL                           |
| CELERY_BROKER_URL            | XXXX                     | Rabbitmq URL                                |
| MAESTRO_MONGO_URI            | mongodb://localhost      | Mongo URI                                   |
| MAESTRO_MONGO_DATABASE       | maestro-client           | Mongo Database name                         |
|                              |                          |                                             |
| MAESTRO_SECRETJWT_PRIVATE    | XXX                      | Secret Key - JWT private connections        |
| MAESTRO_NOAUTH               | XXX                      | Secret Pass to validate private connections |

		


### Contribute ###

Are you interested in developing Maestro Server, creating new features or extending them?

We created a set of documentation, explaining how to set up your development environment, coding styles, standards, learn about the architecture and more. Welcome to the team and contribute with us.

[See our developer guide](http://docs.maestroserver.io/en/latest/contrib.html)

### Contact ###

We may be able to resolve support queries via email. [Please send me a message here](https://maestroserver.typeform.com/to/vf6sGR)

### Donate ###

I have made Maestro Server with my heart, think to solve a real operation IT problem. Its not easy, take time and resources.

The donation will be user to:

- Create new features, implement new providers.
- Maintenance libs, securities flaws, and technical points.

<a href="https://www.buymeacoffee.com/9lVypB7WQ" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

### Sponsor ###

[<img src="docs/_imgs/jetbrains.png" width="100">](https://www.jetbrains.com/?from=maestroserver) 
