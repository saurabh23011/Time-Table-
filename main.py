from flask import Flask, render_template, request, jsonify
import json
import random
from datetime import datetime

app = Flask(__name__)

# Sample data structure
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
TIME_SLOTS = [
    '9:00 AM - 10:00 AM',
    '10:00 AM - 11:00 AM',
    '11:00 AM - 12:00 PM',
    '12:00 PM - 1:00 PM',
    '1:00 PM - 2:00 PM',
    '2:00 PM - 3:00 PM',
    '3:00 PM - 4:00 PM'
]

def load_data():
    """Load data from JSON file or return default data"""
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'subjects': ['Mathematics', 'Physics', 'Chemistry', 'English', 'Computer Science'],
            'teachers': ['Dr. Smith', 'Prof. Johnson', 'Dr. Williams', 'Ms. Brown', 'Mr. Davis'],
            'rooms': ['Room 101', 'Room 102', 'Room 103', 'Lab 1', 'Lab 2']
        }

def save_data(data):
    """Save data to JSON file"""
    with open('data.json', 'w') as f:
        json.dump(data, indent=2, fp=f)

def generate_timetable(subjects, teachers, rooms):
    """Generate a random timetable"""
    timetable = {}
    
    for day in DAYS:
        timetable[day] = []
        available_subjects = subjects.copy()
        
        for time_slot in TIME_SLOTS:
            if time_slot == '12:00 PM - 1:00 PM':
                # Lunch break
                timetable[day].append({
                    'time': time_slot,
                    'subject': 'Lunch Break',
                    'teacher': '-',
                    'room': '-'
                })
            elif available_subjects:
                subject = random.choice(available_subjects)
                teacher = random.choice(teachers)
                room = random.choice(rooms)
                
                timetable[day].append({
                    'time': time_slot,
                    'subject': subject,
                    'teacher': teacher,
                    'room': room
                })
                
                available_subjects.remove(subject)
            else:
                timetable[day].append({
                    'time': time_slot,
                    'subject': 'Free Period',
                    'teacher': '-',
                    'room': '-'
                })
    
    return timetable

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index1.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate a new timetable"""
    data = load_data()
    timetable = generate_timetable(
        data['subjects'],
        data['teachers'],
        data['rooms']
    )
    return jsonify({
        'success': True,
        'timetable': timetable,
        'days': DAYS,
        'time_slots': TIME_SLOTS
    })

@app.route('/data', methods=['GET', 'POST'])
def manage_data():
    """Get or update configuration data"""
    if request.method == 'GET':
        return jsonify(load_data())
    else:
        data = request.json
        save_data(data)
        return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)