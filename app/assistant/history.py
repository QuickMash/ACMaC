import json

class History:
    def __init__(self, file):
        self.file = file
        self.history = self.load_history()

    def load_history(self):
        try:
            with open(self.file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
    def save_history(self):
        with open(self.file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_entry(self, entry):
        self.history.append(entry)
        self.save_history()

    def get_history(self):
        return self.history