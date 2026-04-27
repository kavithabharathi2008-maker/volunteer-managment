import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import csv
import io
from datetime import datetime

from models import db, Volunteer, Task
from utils.matching import calculate_priority_score, match_volunteers_to_task
from utils.chatbot import get_chatbot_response

app = Flask(__name__)
# Secret key for sessions/flash messages
app.config['SECRET_KEY'] = 'hackathon_super_secret_key'

# Configure Database
# By default, use SQLite for easy local setup.
# To use MySQL, uncomment the following line and add your credentials:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables before first request
with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    # Fetch data for dashboard charts and maps
    tasks = Task.query.all()
    volunteers = Volunteer.query.all()
    
    # Calculate stats
    total_tasks = len(tasks)
    pending_tasks = len([t for t in tasks if t.status == 'Pending'])
    total_volunteers = len(volunteers)
    
    # Simple aggregation for charts
    issue_counts = {}
    urgency_counts = {1:0, 2:0, 3:0, 4:0, 5:0}
    
    for task in tasks:
        issue_counts[task.issue_type] = issue_counts.get(task.issue_type, 0) + 1
        urgency_counts[task.urgency_level] += 1
        
    return render_template('dashboard.html', 
                           tasks=tasks, 
                           stats={'total': total_tasks, 'pending': pending_tasks, 'volunteers': total_volunteers},
                           issue_counts=issue_counts,
                           urgency_counts=urgency_counts)

@app.route('/data_collection', methods=['GET', 'POST'])
def data_collection():
    if request.method == 'POST':
        if 'csv_file' in request.files and request.files['csv_file'].filename != '':
            # Handle file upload
            file = request.files['csv_file']
            try:
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_input = csv.DictReader(stream)
                for index, row in enumerate(csv_input):
                    new_task = Task(
                        title=row.get('Title', f"Issue {index}"),
                        description=row.get('Description', ''),
                        issue_type=row.get('Issue Type', 'Other'),
                        urgency_level=int(row.get('Urgency', 1) if row.get('Urgency') else 1),
                        location=row.get('Location', 'Unknown'),
                        latitude=float(row.get('Latitude')) if row.get('Latitude') else None,
                        longitude=float(row.get('Longitude')) if row.get('Longitude') else None
                    )
                    new_task.priority_score = calculate_priority_score(new_task)
                    db.session.add(new_task)
                db.session.commit()
                flash('CSV data successfully imported!', 'success')
            except Exception as e:
                flash(f'Error processing CSV: {str(e)}', 'danger')
        else:
            # Handle manual entry form
            title = request.form.get('title')
            description = request.form.get('description')
            issue_type = request.form.get('issue_type')
            urgency_level = int(request.form.get('urgency_level'))
            location = request.form.get('location')
            
            new_task = Task(
                title=title,
                description=description,
                issue_type=issue_type,
                urgency_level=urgency_level,
                location=location
            )
            new_task.priority_score = calculate_priority_score(new_task)
            
            db.session.add(new_task)
            db.session.commit()
            flash('New task successfully reported!', 'success')
            
        return redirect(url_for('tasks'))
        
    return render_template('data_collection.html')

@app.route('/tasks')
def tasks():
    # Get all tasks, sorted by highest priority first
    all_tasks = Task.query.order_by(Task.priority_score.desc()).all()
    return render_template('tasks.html', tasks=all_tasks)

@app.route('/volunteers', methods=['GET', 'POST'])
def volunteers():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        skills = request.form.get('skills')
        location = request.form.get('location')
        availability = request.form.get('availability')
        
        new_vol = Volunteer(name=name, email=email, skills=skills, location=location, availability=availability)
        db.session.add(new_vol)
        db.session.commit()
        flash('Volunteer successfully registered!', 'success')
        return redirect(url_for('volunteers'))
        
    all_volunteers = Volunteer.query.all()
    return render_template('volunteers.html', volunteers=all_volunteers)

@app.route('/match/<int:task_id>', methods=['GET'])
def match_volunteers(task_id):
    task = Task.query.get_or_404(task_id)
    all_volunteers = Volunteer.query.all()
    matches = match_volunteers_to_task(task, all_volunteers)
    
    return render_template('matching.html', task=task, matches=matches)

@app.route('/assign/<int:task_id>/<int:volunteer_id>', methods=['POST'])
def assign_volunteer(task_id, volunteer_id):
    task = Task.query.get_or_404(task_id)
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    
    task.assigned_volunteer_id = volunteer.id
    task.status = 'In Progress'
    db.session.commit()
    
    flash(f'Task assigned to {volunteer.name}!', 'success')
    return redirect(url_for('tasks'))

@app.route('/chatbot/api', methods=['POST'])
def chatbot_api():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'Please provide a message.'}), 400
        
    # Gather a little context for the bot
    pending_tasks_count = Task.query.filter_by(status='Pending').count()
    context = f"Currently, there are {pending_tasks_count} pending tasks needing volunteers."
    
    bot_response = get_chatbot_response(user_message, context)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    # Fix import error for url_form -> url_for
    app.run(debug=True)
