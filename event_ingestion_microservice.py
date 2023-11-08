import os

import pika
from flask import Flask, request, jsonify
from db_crud import EventsCRUD, RulesCRUD
from event_processing import ComparingEventProcessing
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
    result['status'] = 'Event Checked'
    return jsonify(result), 201


@app.route('/rules', methods=['POST'])
def create_rule():
    rule_data = request.get_json()
    result = rules_crud.create_rule(rule_data)
    result['status'] = 'Rule Created'
    return jsonify(result), 201


if __name__ == '__main__':
    db_connection_params = {
        'host': os.getenv('DB_HOST', '0.0.0.0'),
        'port': int(os.getenv('DB_PORT', '5432')),
        'dbname': os.getenv('DB_NAME', 'cep'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASS', 'postgres'),
    }

    events_crud = EventsCRUD(**db_connection_params)
    rules_crud = RulesCRUD(**db_connection_params)
    cep = ComparingEventProcessing(events_crud, rules_crud)

    msg_broker_host = os.getenv('MESSAGE_BROKER_HOST', '0.0.0.0')
    msg_broker_port = os.getenv('MESSAGE_BROKER_PORT', '5672')
    msg_broker_user = os.getenv('MESSAGE_BROKER_USER', 'guest')
    msg_broker_pass = os.getenv('MESSAGE_BROKER_PASS', 'guest')
    msg_broker_name = os.getenv('MESSAGE_BROKER_NAME', 'event_queue')

    amqp_url = f'amqp://{msg_broker_user}:{msg_broker_pass}@{msg_broker_host}:{msg_broker_port}/%2F'
    params = pika.URLParameters(amqp_url)

    msg_broker = ProducerMessageBroker(params, msg_broker_name)
    msg_broker.open_connection()

    print("Starting Server")
    app.run(host='0.0.0.0')
