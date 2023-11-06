# Comparing Event Processing and Rule Engines

## Introduction
This app provides a simple REST API for creating rules to process and events to compare. 
It integrates with RabbitMQ as a message broker to handle event-driven operations 
and includes CRUD operations interacting with a PostgreSQL database.

## Microservices
- **Event Ingestion**: Handles the ingestion of events into the system.
- **Event Processing**: Processes the events according to defined rules and triggers alerts.
- **Alert and Notification**: Sends out notifications based on the processed events.

## Features
- **CRUD REST API**
- **Docker Integration**: Designed to run within a Docker container for easy deployment.

## Installation
Before installation, ensure that Docker and Python are installed on your system.
1. Clone the repository or download the application files.
    ```bash
   git clone https://github.com/DaniHaimov/EltaCEP.git
   ```
2. Make sure ports 5432 and 5672 are available, you can stop them or choose other ports:
    ```bash
    systemctl stop postgresql
    systemctl stop rabbitmq-server.service
   ```

## Configuration
Before running the application, configure the environment variables. Create a `.env` file in the root directory and set the following variables:
```dotenv
PORT=<app_port>

DB_HOST=<your_db_host>#postgresdb
DB_PORT=<your_db_port>#5432
DB_USER=<your_db_user>#postgres
DB_PASS=<your_db_password>#postgres
DB_NAME=<your_db_name>#cep
MESSAGE_BROKER_HOST=<your_broker_host>#rabbitmq
MESSAGE_BROKER_PORT=<your_broker_port>#5672
MESSAGE_BROKER_NAME=<your_broker_name>#event_queue
```
If you want to change the default port, you can change it in the `compose.yml` file

## Running the Application
```bash
docker compose up --build
docker-compose up --build #for old versions
```

## Stop the Application
```bash
docker compose down 
#if you want remove to remove the volumes add --volumes flag
```
## Diagrams
### Services Diagram
![Services Diagram](/diagrams/ProjectDiagrams-services.drawio.png)

### Services Diagram
![Services Diagram](/diagrams/ProjectDiagrams-tables.drawio.png)

## Endpoints
The application provides endpoints for event management with JSON responses:
* `POST` /rules: Create a new rule.</br>
This endpoint is used to create a new rule. 
The request must include the rule details in JSON format. 
The rule stored on DB for future processes.
    #### Request:
    ```json
    POST /api/events
    Content-Type: application/json
    {
      "device": "device_name",
      "sensor_type":  "sensor_name",
      "operator": "L",
      "unusual_value": 42, // if compare_to_last_event it's calculate the diff in seconds
      "rule_description": "device_name: sensor higher than 42",
      // optional
      "compare_to_last_event": false
    }
  ```
  #### Successful Response:
    ```json
    HTTP/1.1 201 Created
    Content-Type: application/json
    {
      "rule_id": "123e4567-e89b-12d3-a456-426655440000"
      "status": "Rule Created",
    }
  ```
  #### Valid operators:
  ```text
  E, NE, G, NG, EG, NEG, L, NL, EL, NEL
  N - Not
  E - Equal
  G - Greater
  L - Lower
  ```
  
* `POST` /events: Create a new event.</br>
This endpoint is used to create a new event. 
The request must include the event details in JSON format. 
The event stored on DB and delivered to `Event Processing` to process rules and if is unusual it is delivered to RabbitMQ for notification by `Alert and Notification`.
    #### Request:
    ```json
    POST /api/events
    Content-Type: application/json
    {
      "device": "device_name",
      "sensor_type": "sensor_name",
      "sensor_value": 42
    }
  ```
  #### Successful Response:
    ```json
    HTTP/1.1 201 Created
    Content-Type: application/json
    {
      "event_id": "123e4567-e89b-12d3-a456-426655440000"
      "status": "Event Checked",
    }
  ```

## Dependencies
This application requires the following Python packages:
* flask
* pika
* psycopg2-binary
* dotenv
* requests

Install dependencies using `pip`:
```bash
pip install -r requirements.txt
```

## Notes Limitations
1. When composing the project on docker, it's failed to connect to RabbitMQ container you can run the services in your remote:
    ```bash
    python3 ./event_ingestion_microservice.py &
    python3 ./alert_and_notification_microservice.py &
    ```
2. Drone simulator is on development.