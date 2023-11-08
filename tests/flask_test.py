import requests

if __name__ == '__main__':
    base_url = 'http://127.0.0.1:5000'

    # requests.post(url=f'{base_url}/rules', json={
    #     "device": "car",
    #     "sensor_type":  "engine heat",
    #     "operator": "G",
    #     "unusual_value": 300,
    #     "rule_description": "Car's engine heat greater than 300",
    #     "compare_to_last_event": False
    # })

    requests.post(url=f'{base_url}/events', json={
        "device": "car",
        "sensor_type":  "engine heat",
        "sensor_value": 301
    })
