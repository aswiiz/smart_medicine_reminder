from flask import Flask, request, jsonify, send_from_directory
from med_manager import med_manager

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/setup.html')
def setup():
    return send_from_directory('static', 'setup.html')

@app.route('/dashboard.html')
def dashboard():
    return send_from_directory('static', 'dashboard.html')

@app.route('/speaker.html')
def speaker():
    return send_from_directory('static', 'speaker.html')

@app.route('/api/setup', methods=['POST'])
def api_setup():
    data = request.json
    action = data.get('action')
    
    if action == 'add_med':
        med_manager.add_medicine(data.get('name'), data.get('stock'))
    elif action == 'add_schedule':
        med_manager.add_schedule(data.get('med_name'), data.get('time'), data.get('dosage'))
    
    return jsonify({'status': 'success'})

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(med_manager.get_config())

@app.route('/api/action', methods=['POST'])
def take_action():
    data = request.json
    med_name = data.get('med_name')
    dosage = data.get('dosage')
    
    # If type is 'missed', just log it
    if data.get('type') == 'missed':
        med_manager.log_event("ALERT", f"MISSED DOSE: {med_name} at {data.get('time')}. Notification sent to Caretaker.")
        return jsonify({'status': 'logged_missed'})
        
    success = med_manager.record_taken(med_name, dosage)
    return jsonify({'status': 'success' if success else 'failed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
