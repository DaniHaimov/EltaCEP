import os
from datetime import datetime
from dotenv import load_dotenv

from db_crud import EventsCRUD, RulesCRUD
from event_processing import ComparingEventProcessing

load_dotenv()

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
    cep = ComparingEventProcessing(events_crud, rules_crud)

    new_rule = {
        "device": "Car3",
        "sensor_type": "Speed",
        "operator": "G",
        "unusual_value": 20,
        "rule_description": "Car3: Accelerated more than 20 km/h on average per second",
        "compare_to_last_event": True}
    # rules_crud.create_rule(new_rule)

    for rule in rules_crud.read_specific_sensor_rules(new_rule):
        # print(rule)
        pass

    new_event = {
        "device": "Car3",
        "sensor_type": "Speed",
        "sensor_value": 3000000
    }
    last_sensor_event = events_crud.read_last_sensor_event(new_event)
    if last_sensor_event is not None:
        time_difference = datetime.utcnow() - last_sensor_event['created_at']
        print(time_difference.total_seconds())
        print(last_sensor_event['sensor_value'], last_sensor_event['created_at'])

    for rule_id in cep.check_event(new_event):
        print(rules_crud.get_rule_description(rule_id))
    # events_crud.create_event(new_event)
