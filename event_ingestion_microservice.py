import os
from flask import Flask, request, jsonify
from db_crud import EventsCRUD, RulesCRUD
from event_processing import CEP
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/events', methods=['POST'])
def create_event():
    event_data = request.get_json()
    result = events_crud.create_event(event_data)
    unusual_events = cep.check_event(event_data)
    # TODO: send unusual_events to message broker
    return jsonify(result), 201


@app.route('/rules', methods=['POST'])
def create_rule_route():
    rule_data = request.get_json()
    result = rules_crud.create_rule(rule_data)
    return jsonify(result), 201


if __name__ == '__main__':
    db_connection_params = {
        "host": os.getenv('DB_HOST'),
        "port": os.getenv('DB_PORT'),
        "dbname": os.getenv('DB_NAME'),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASS'),
    }

    events_crud = EventsCRUD(**db_connection_params)
    rules_crud = RulesCRUD(**db_connection_params)
    cep = CEP(events_crud, rules_crud)

    app.run()
