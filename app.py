import os
import subprocess

if __name__ == '__main__':
    subprocess.Popen(["python3", "./event_ingestion_microservice.py &"])
    subprocess.run(["python3", "./alert_and_notification_microservice.py"])
