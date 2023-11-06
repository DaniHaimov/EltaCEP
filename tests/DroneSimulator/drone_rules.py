import requests


def add_rules():
    requests.post('http://127.0.0.1:5000/rules', json={
        "device": "drone",
        "sensor_type":  "height",
        "operator": "G",
        "unusual_value": 100,
        "rule_description": "drone: higher than 100",
        "compare_to_last_event": False
    })

