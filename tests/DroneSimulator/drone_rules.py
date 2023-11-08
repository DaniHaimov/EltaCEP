import tkinter as tk
import requests


class RulesGUI:
    def __init__(self, root, _rules_url):
        self.root = root
        self.rules_url = _rules_url
        self.root.title("Rules GUI")
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.data = {"device": None,
                     "sensor_type": None,
                     "operator": None,
                     "unusual_value": None,
                     "rule_description": None,
                     "compare_to_last_event": None,
                     }
        self.entries = dict()
        self.update_labels()

    def update_labels(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for key in self.data.keys():
            key_label = tk.Label(self.frame, text=key)
            key_label.grid(row=len(self.entries), column=0, padx=5, pady=5)
            entry = tk.Entry(self.frame)
            entry.grid(row=len(self.entries), column=1, padx=5, pady=5)
            self.entries[key] = entry

        # "compare_to_last_event": None
        # key_label = tk.Label(self.frame, text="compare_to_last_event")
        # key_label.grid(row=len(self.entries), column=0, padx=5, pady=5)
        # entry = tk.Entry(self.frame)
        # entry.grid(row=len(self.entries), column=1, padx=5, pady=5)
        # self.entries["compare_to_last_event"] = bool(entry)

        send_button = tk.Button(self.frame, text="Add Rule", command=lambda: self.add_rule())
        send_button.grid(row=len(self.entries), column=1, padx=5, pady=5)



    def add_rule(self):
        for key, value in self.entries.items():
            self.entries[key] = value.get()
        print(self.entries)
        requests.post(self.rules_url, json=self.entries)


def add_rule(self, sensor_type: str, operator: str, unusual_value, rule_description, compare_to_last_event: bool = False):
    requests.post(self.rules_url, json={
        "device": "drone",
        "sensor_type": sensor_type,
        "operator": operator,
        "unusual_value": unusual_value,
        "rule_description": rule_description,
        "compare_to_last_event": compare_to_last_event
    })


def add_rules():
    add_rule("height", "G", 100, "drone: higher than 100")


if __name__ == '__main__':
    # rules_url = 'http://127.0.0.1:5000/rules'
    # root = tk.Tk()
    # app = RulesGUI(root, rules_url)
    #
    # root.mainloop()
    add_rules()

