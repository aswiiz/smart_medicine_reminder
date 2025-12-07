import json
import os
import datetime
from datetime import datetime as dt

DATA_FILE = 'data.json'

class MedManager:
    def __init__(self):
        self.medicines = []
        self.schedules = []
        self.logs = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.medicines = data.get('medicines', [])
                    self.schedules = data.get('schedules', [])
                    self.logs = data.get('logs', [])
            except:
                self.save_data()
        else:
            self.save_data()

    def save_data(self):
        data = {
            'medicines': self.medicines,
            'schedules': self.schedules,
            'logs': self.logs
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def log_event(self, type, message):
        event = {
            'type': type,
            'message': message,
            'timestamp': dt.now().isoformat()
        }
        self.logs.insert(0, event)
        self.logs = self.logs[:50] # Keep last 50 logs
        self.save_data()

    def add_medicine(self, name, stock):
        # Update if exists
        for med in self.medicines:
            if med['name'].lower() == name.lower():
                med['stock'] = int(stock)
                self.save_data()
                return
        self.medicines.append({
            'name': name,
            'stock': int(stock),
            'low_threshold': 5
        })
        self.save_data()

    def add_schedule(self, med_name, time, dosage):
        self.schedules.append({
            'med_name': med_name,
            'time': time, # "HH:MM" 24h format
            'dosage': int(dosage)
        })
        self.save_data()
    
    def get_config(self):
        return {
            'medicines': self.medicines,
            'schedules': self.schedules,
            'logs': self.logs
        }
    
    def record_taken(self, med_name, dosage):
        for med in self.medicines:
            if med['name'].lower() == med_name.lower():
                med['stock'] -= int(dosage)
                if med['stock'] < 0: med['stock'] = 0
                
                self.log_event("ACTION", f"Taken: {dosage} {med_name}. Remaining: {med['stock']}")
                
                # Check low stock
                if med['stock'] <= med['low_threshold']:
                    self.log_event("ALERT", f"Low Stock Warning: {med_name} has {med['stock']} left. SMS sent to Caretaker.")
                
                self.save_data()
                return True
        return False

    def check_missed_doses(self):
        # In a real app complexity is higher (checking if taken today etc).
        # For this prototype/simulation, the frontend 'Speaker' drives the time/reminders.
        # We will expose an endpoint to log a missed dose if the frontend decides it was missed.
        pass

med_manager = MedManager()
