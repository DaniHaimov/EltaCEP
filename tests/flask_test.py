import requests

if __name__ == '__main__':
    base_url = 'http://localhost:5000'

    requests.post(url=f'{base_url}/rules', json={
        "device": "device_name",
        "sensor_type":  "sensor_name",
        "operator": "L",
        "unusual_value": 42,
        "rule_description": "device_name: sensor higher than 42",
        "compare_to_last_event": False
    })

    requests.post(url=f'{base_url}/events', json={
        "device": "device_name",
        "sensor_type":  "sensor_name",
        "sensor_value": 20
    })
