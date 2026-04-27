import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
import csv
import io
from datetime import datetime

from models import db, User, Issue, Volunteer, Task
from utils.matching import calculate_priority_score, match_volunteers_to_issue
from utils.chatbot import get_chatbot_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackathon_super_secret_key'

# Configure Database
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///community.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    try:
        db.create_all()
        # Create a default admin user if none exists
        if not User.query.filter_by(role='Admin').first():
            admin = User(name="Admin", email="admin@example.com", role="Admin", password_hash="admin123")
            db.session.add(admin)
            db.session.commit()
    except Exception as e:
        print(f"Database initialization warning: {e}")

# --- Helper: Get Current User ---
def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        role = request.form.get('role')
        user = User.query.filter_by(email=email, role=role).first()
        if user:
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash(f'Welcome back, {user.name}!', 'success')
            if user.role == 'NGO':
                return redirect(url_for('ngo_dashboard'))
            elif user.role == 'Volunteer':
                return redirect(url_for('volunteer_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials or role.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        location = request.form.get('location')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'warning')
            return redirect(url_for('register'))
            
        new_user = User(name=name, email=email, role=role, location=location)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- NGO Dashboard ---
@app.route('/ngo_dashboard', methods=['GET', 'POST'])
def ngo_dashboard():
    user = get_current_user()
    if not user or user.role != 'NGO':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        if 'csv_file' in request.files and request.files['csv_file'].filename != '':
            file = request.files['csv_file']
            try:
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_input = csv.DictReader(stream)
                for row in csv_input:
                    new_issue = Issue(
                        location=row.get('Location', user.location),
                        category=row.get('Category', 'Other'),
                        urgency=int(row.get('Urgency', 1)),
                        description=row.get('Description', ''),
                        latitude=float(row.get('Latitude')) if row.get('Latitude') else None,
                        longitude=float(row.get('Longitude')) if row.get('Longitude') else None,
                        reported_by_id=user.id
                    )
                    db.session.add(new_issue)
                    db.session.flush() # Get ID for Task
                    new_task = Task(issue_id=new_issue.id, priority_score=calculate_priority_score(new_issue))
                    db.session.add(new_task)
                db.session.commit()
                flash('CSV data successfully imported!', 'success')
            except Exception as e:
                flash(f'Error processing CSV: {str(e)}', 'danger')
        else:
            category = request.form.get('category')
            urgency = int(request.form.get('urgency'))
            location = request.form.get('location')
            description = request.form.get('description')
            
            new_issue = Issue(category=category, urgency=urgency, location=location, description=description, reported_by_id=user.id)
            db.session.add(new_issue)
            db.session.flush()
            new_task = Task(issue_id=new_issue.id, priority_score=calculate_priority_score(new_issue))
            db.session.add(new_task)
            db.session.commit()
            
            if urgency >= 4:
                flash('CRITICAL: High urgency issue reported! Admin has been alerted.', 'warning')
            else:
                flash('Issue successfully reported!', 'success')
        
    my_issues = Issue.query.filter_by(reported_by_id=user.id).all()
    return render_template('ngo_dashboard.html', issues=my_issues)

# --- Volunteer Dashboard ---
@app.route('/volunteer_dashboard', methods=['GET', 'POST'])
def volunteer_dashboard():
    user = get_current_user()
    if not user or user.role != 'Volunteer':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
        
    volunteer = Volunteer.query.filter_by(user_id=user.id).first()
    
    if request.method == 'POST':
        skills = request.form.get('skills')
        availability = request.form.get('availability')
        location = request.form.get('location')
        
        if volunteer:
            volunteer.skills = skills
            volunteer.availability = availability
            volunteer.location = location
        else:
            volunteer = Volunteer(user_id=user.id, name=user.name, skills=skills, availability=availability, location=location)
            db.session.add(volunteer)
        db.session.commit()
        flash('Profile updated!', 'success')
        
    my_tasks = Task.query.filter_by(volunteer_id=volunteer.id if volunteer else -1).all()
    return render_template('volunteer_dashboard.html', volunteer=volunteer, tasks=my_tasks)

@app.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    status = request.form.get('status')
    if status in ['Pending', 'In Progress', 'Completed']:
        task.status = status
        db.session.commit()
        flash('Status updated!', 'success')
    return redirect(url_for('volunteer_dashboard'))

# --- Admin Dashboard ---
@app.route('/admin_dashboard')
def admin_dashboard():
    user = get_current_user()
    if not user or user.role != 'Admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
        
    tasks = Task.query.all()
    volunteers = Volunteer.query.all()
    
    # Intelligence: Top 5 Critical Needs
    critical_needs = Task.query.join(Issue).order_by(Task.priority_score.desc()).limit(5).all()
    
    # Stats for charts
    category_counts = {}
    urgency_counts = {1:0, 2:0, 3:0, 4:0, 5:0}
    area_counts = {}
    
    for t in tasks:
        category_counts[t.issue.category] = category_counts.get(t.issue.category, 0) + 1
        urgency_counts[t.issue.urgency] += 1
        area_counts[t.issue.location] = area_counts.get(t.issue.location, 0) + 1
        
    return render_template('dashboard.html', 
                           tasks=tasks, 
                           volunteers=volunteers,
                           critical_needs=critical_needs,
                           category_counts=category_counts,
                           urgency_counts=urgency_counts,
                           area_counts=area_counts)

@app.route('/match/<int:task_id>')
def match_volunteers(task_id):
    task = Task.query.get_or_404(task_id)
    all_volunteers = Volunteer.query.all()
    matches = match_volunteers_to_issue(task.issue, all_volunteers)
    return render_template('matching.html', task=task, matches=matches)

@app.route('/assign/<int:task_id>/<int:volunteer_id>', methods=['POST'])
def assign_task(task_id, volunteer_id):
    task = Task.query.get_or_404(task_id)
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    
    task.volunteer_id = volunteer.id
    task.status = 'In Progress'
    db.session.commit()
    
    flash(f'Task assigned to {volunteer.name}!', 'success')
    # Simulated notification
    return redirect(url_for('admin_dashboard'))

@app.route('/map')
def map_view():
    tasks = Task.query.all()
    return render_template('map.html', tasks=tasks)

@app.route('/chatbot/api', methods=['POST'])
def chatbot_api():
    user_message = request.json.get('message', '')
    pending_count = Task.query.filter_by(status='Pending').count()
    context = f"Currently, there are {pending_count} pending tasks."
    return jsonify({'response': get_chatbot_response(user_message, context)})

if __name__ == '__main__':
    app.run(debug=True)
