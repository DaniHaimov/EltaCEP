from datetime import datetime
import requests


class Drone:
    def __init__(self,
                 latitude=0.0,
                 latitude_speed=0.0,
                 longitude=0.0,
                 longitude_speed=0.0,
                 height=0.0,
                 height_speed=0.0,
                 cpu_usage=0.0,
                 temperature=0.0):
        self.sensors = {
            'latitude': latitude,
            'latitude_speed': latitude_speed,
            'longitude': longitude,
            'longitude_speed': longitude_speed,
            'height': height,
            'height_speed': height_speed,
            'cpu_usage': cpu_usage,
            'temperature': temperature,
        }
        self.last_update = datetime.utcnow()

    def send_event(self, sensor: str):
        requests.post('http://127.0.0.1:5000/events', json={
            "device": "drone",
            "sensor_type": sensor,
            "sensor_value": self.sensors[sensor]
        })

    def send_events(self):
        for sensor in self.sensors.keys():
            self.send_event(sensor)

    def update(self):
        current_time = datetime.utcnow()
        time_difference = (current_time - self.last_update).total_seconds()
        self.last_update = current_time

        self.sensors['latitude'] += (self.sensors['latitude_speed'] * time_difference)
        self.sensors['longitude'] += (self.sensors['longitude_speed'] * time_difference)
        self.sensors['height'] += (self.sensors['height_speed'] * time_difference)

    def get_sensors(self) -> dict:
        return self.sensors.copy()
