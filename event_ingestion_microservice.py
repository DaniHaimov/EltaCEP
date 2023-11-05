import os

import pika
from flask import Flask, request, jsonify
from db_crud import EventsCRUD, RulesCRUD
from event_processing import CEP
from dotenv import load_dotenv

from message_broker import ProducerMessageBroker

load_dotenv()
app = Flask(__name__)


def send_unusual_events(unusual_rules):
    for rule in unusual_rules:
        rule_description = rules_crud.get_rule_description(rule)
        msg_broker.publish(rule_description)


@app.route('/events', methods=['POST'])
def create_event():
    event_data = request.get_json()

    unusual_rules = cep.check_event(event_data)
    send_unusual_events(unusual_rules)

    result = events_crud.create_event(event_data)
    return jsonify(result), 201


@app.route('/rules', methods=['POST'])
def create_rule_route():
    rule_data = request.get_json()
    result = rules_crud.create_rule(rule_data)
    return jsonify(result), 201


if __name__ == '__main__':
    db_connection_params = {
        "host": os.getenv('DB_HOST'),
        "port": int(os.getenv('DB_PORT')),
        "dbname": os.getenv('DB_NAME'),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASS'),
    }

    events_crud = EventsCRUD(**db_connection_params)
    rules_crud = RulesCRUD(**db_connection_params)
    cep = CEP(events_crud, rules_crud)

    msg_broker_host = os.getenv("MESSAGE_BROKER_HOST")
    msg_broker_port = os.getenv("MESSAGE_BROKER_PORT")
    msg_broker_user = os.getenv("MESSAGE_BROKER_USER")
    msg_broker_pass = os.getenv("MESSAGE_BROKER_PASS")
    msg_broker_name = os.getenv("MESSAGE_BROKER_NAME")

    # amqp_url = f'amqp://{msg_broker_user}:{msg_broker_pass}@{msg_broker_host}:{msg_broker_port}/v%2fhost'
    # params = pika.URLParameters(amqp_url)

    params = pika.ConnectionParameters(host=msg_broker_host)

    msg_broker = ProducerMessageBroker(params, msg_broker_name)
    msg_broker.open_connection()

    app.run()
