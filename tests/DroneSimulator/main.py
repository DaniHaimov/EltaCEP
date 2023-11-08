import threading
import time

from tests.DroneSimulator.drone import Drone
# from tests.DroneSimulator.drone_rules import add_rules

import tkinter as tk


class DroneGUI:
    def __init__(self, root, drone: Drone):
        self.root = root
        self.drone = drone
        self.entries = {}

        self.root.title("Drone GUI")

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.update_labels()

    def update_labels(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        data = self.drone.get_sensors()
        self.entries = {}
        for key, value in data.items():
            key_label = tk.Label(self.frame, text=key)
            key_label.grid(row=len(self.entries), column=0, padx=5, pady=5)
            value_label = tk.Label(self.frame, text=str(value))
            value_label.grid(row=len(self.entries), column=1, padx=5, pady=5)
            entry = tk.Entry(self.frame)
            entry.grid(row=len(self.entries), column=2, padx=5, pady=5)
            send_button = tk.Button(self.frame, text="Update", command=lambda k=key: self.update_data(k))
            send_button.grid(row=len(self.entries), column=3, padx=5, pady=5)
            send_button = tk.Button(self.frame, text="Send Event", command=lambda k=key: self.send_event(k))
            send_button.grid(row=len(self.entries), column=4, padx=5, pady=5)
            self.entries[key] = entry

        send_button = tk.Button(self.frame, text="Update Drone State", command=lambda: self.update_sensors())
        send_button.grid(row=len(self.entries), column=1, padx=5, pady=5)
        send_button = tk.Button(self.frame, text="Send Sensors Events", command=lambda: self.drone.send_events())
        send_button.grid(row=len(self.entries), column=2, padx=5, pady=5)

    def update_data(self, key):
        input_value = self.entries[key].get()
        if input_value.replace(".", "", 1).isdigit():
            input_value = float(input_value)
        self.drone.sensors[key] = input_value
        self.update_labels()

    def send_event(self, key):
        self.drone.send_event(key)

    def update_sensors(self):
        self.drone.update()
        self.update_labels()


if __name__ == "__main__":
    drone = Drone()

    root = tk.Tk()
    app = DroneGUI(root, drone)

    root.mainloop()



