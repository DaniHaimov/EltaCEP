from datetime import datetime
import requests


class Drone:
    def __init__(self):
        self.sensors = {
            'latitude': 0.0,
            'latitude_speed': 0.0,
            'longitude': 0.0,
            'longitude_speed': 0.0,
            'height': 0.0,
            'height_speed': 0.0,
            'cpu_usage': 0.0,
            'temperature': 0.0,
        }
        self.last_update = datetime.utcnow()

    def send_events(self):
        for sensor, value in self.sensors.items():
            requests.post('http://127.0.0.1:5000/events', json={
                "device": "drone",
                "sensor_type": sensor,
                "sensor_value": value
            })

    def update(self):
        current_time = datetime.utcnow()
        time_difference = (current_time - self.last_update).total_seconds()
        self.last_update = current_time

        self.sensors['latitude'] += (self.sensors['latitude_speed'] * time_difference)
        self.sensors['longitude'] += (self.sensors['longitude_speed'] * time_difference)
        self.sensors['height'] += (self.sensors['height_speed'] * time_difference)

