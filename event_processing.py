from datetime import datetime
from enum import Enum


class Operators(Enum):
    E = lambda a, b: str(a) == str(b)
    NE = lambda a, b: str(a) != str(b)
    G = lambda a, b: float(a) > float(b)
    NG = lambda a, b: not (float(a) > float(b))
    EG = lambda a, b: float(a) >= float(b)
    NEG = lambda a, b: not (float(a) >= float(b))
    L = lambda a, b: float(a) < float(b)
    NL = lambda a, b: not (float(a) < float(b))
    EL = lambda a, b: float(a) <= float(b)
    NEL = lambda a, b: not (float(a) <= float(b))


class ComparingEventProcessing:
    def __init__(self, events_crud, rules_crud):
        self.events_crud = events_crud
        self.rules_crud = rules_crud

    def check_event(self, event):
        rules = self.rules_crud.read_specific_sensor_rules(event)
        sensor_value = event['sensor_value']
        unusual_events = list()
        for rule in rules:
            rule_operator = rule['operator']
            unusual_value = rule['unusual_value']
            compare_to_last_event = rule['compare_to_last_event']

            checked_value = sensor_value
            if compare_to_last_event:
                last_sensor_event = self.events_crud.read_last_sensor_event(event)
                if last_sensor_event is None:
                    continue
                time_difference = datetime.utcnow() - last_sensor_event['created_at']
                checked_value = float(sensor_value) - float(last_sensor_event['sensor_value'])
                unusual_value = float(unusual_value) * time_difference.total_seconds()

            operator = get_operator(rule_operator)
            if operator(checked_value, unusual_value):
                unusual_events.append(rule['rule_id'])

        return unusual_events




operator_mapping = {
    "E": Operators.E,
    "NE": Operators.NE,
    "G": Operators.G,
    "NG": Operators.NG,
    "EG": Operators.EG,
    "NEG": Operators.NEG,
    "L": Operators.L,
    "NL": Operators.NL,
    "EL": Operators.EL,
    "NEL": Operators.NEL,
}


def get_operator(rule_operator: str):
    return operator_mapping.get(rule_operator, None)
