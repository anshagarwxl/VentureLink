# ========================================
# VENTURELINK FLASK APPLICATION
# Full-stack startup-investor platform with role-based access
# ========================================

from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector

# Flask app initialization with secret key for session security
app = Flask(__name__)
app.secret_key = "venturelink_secret_key_2024"

# ========================================
# DATABASE CONNECTION
# ========================================
# Connect to MySQL database 'venturelink' with existing schema
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Jaguar#500",
    database="venturelink"
)
cursor = db.cursor(dictionary=True)


# ========================================
# 1. LOGIN ROUTE (HOME PAGE)
# Handles role selection (Startup/Investor) and startup ID assignment
# ========================================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        session['role'] = role
        
        if role == 'startup':
            # STARTUP ROLE: Requires startup selection from database
            startup_id = request.form.get('startup_id')
            if startup_id:
                session['startup_id'] = int(startup_id)
            else:
                flash('Please select your startup', 'danger')
                return redirect('/')
        
        return redirect('/dashboard')
    
    # GET: Load all startups for selection dropdown
    cursor.execute("SELECT startup_id, name FROM Startups ORDER BY name")
    all_startups = cursor.fetchall()
    return render_template('login.html', startups=all_startups)


# ========================================
# 2. DASHBOARD - ROLE BASED
# Different content for Startup vs Investor roles
# ========================================
@app.route('/dashboard')
def dashboard():
    role = session.get('role')
    
    if not role:
        return redirect('/')  # Redirect unauthenticated users
    
    # Get global statistics for both roles
    cursor.execute("SELECT COUNT(*) as count FROM Startups")
    total_startups = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM Investors")
    total_investors = cursor.fetchone()['count']
    
    # Featured startups for investor dashboard (random selection)
    cursor.execute("SELECT * FROM Startups ORDER BY RAND() LIMIT 3")
    featured_startups = cursor.fetchall()
    
    # STARTUP ROLE: Load user's startup details
    my_startup = None
    if role == 'startup':
        startup_id = session.get('startup_id')
        if startup_id:
            cursor.execute("SELECT * FROM Startups WHERE startup_id = %s", (startup_id,))
            my_startup = cursor.fetchone()
    
    # Load all startups for dropdown
    cursor.execute("SELECT startup_id, name FROM Startups ORDER BY name")
    all_startups = cursor.fetchall()
    
    return render_template('dashboard.html',
                      role=role,
                      total_startups=total_startups,
                      total_investors=total_investors,
                      my_startup=my_startup,
                      all_startups=all_startups,
                      startups=featured_startups)


# ========================================
# 3. STARTUPS MANAGEMENT PAGE
# Role-based CRUD operations with ownership check
# ========================================
@app.route('/startups')
def startups():
    role = session.get('role')
    
    if not role:
        return redirect('/')
    
    cursor.execute("SELECT * FROM Startups ORDER BY name")
    data = cursor.fetchall()
    
    return render_template('startups.html', startups=data, role=role)


# ========================================
# 4. ADD NEW STARTUP (STARTUP ROLE ONLY)
# ========================================
@app.route('/add', methods=['POST'])
def add():
    role = session.get('role')
    
    if role != 'startup':
        flash('Access denied - Only startups can add', 'danger')
        return redirect('/startups')
    
    try:
        cursor.execute(
            "INSERT INTO Startups (name, city, stage, valuation) VALUES (%s,%s,%s,%s)",
            (request.form['name'], request.form['city'],
             request.form['stage'], request.form['valuation'])
        )
        db.commit()
        flash('Startup added successfully!', 'success')
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
    
    return redirect('/startups')


# ========================================
# 5. DELETE STARTUP (OWNERSHIP CHECK)
# Startup can only delete their own startup
# ========================================
@app.route('/delete/<int:id>')
def delete(id):
    role = session.get('role')
    
    if role != 'startup':
        flash('Access denied - Investors cannot delete', 'danger')
        return redirect('/startups')
    
    startup_id = session.get('startup_id')
    
    if startup_id != id:
        flash('Ownership violation - You can only delete your own startup', 'danger')
        return redirect('/startups')
    
    cursor.execute("DELETE FROM Startups WHERE startup_id=%s", (id,))
    db.commit()
    flash('Startup deleted successfully!', 'success')
    return redirect('/startups')


# ========================================
# 6. UPDATE STARTUP (OWNERSHIP CHECK)
# Startup can only update their own startup
# ========================================
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    role = session.get('role')
    
    if role != 'startup':
        flash('Access denied - Investors cannot update', 'danger')
        return redirect('/startups')
    
    startup_id = session.get('startup_id')
    
    if startup_id != id:
        flash('Ownership violation - You can only edit your own startup', 'danger')
        return redirect('/startups')
    
    cursor.execute(
        "UPDATE Startups SET name=%s, city=%s, stage=%s, valuation=%s WHERE startup_id=%s",
        (request.form['name'], request.form['city'],
         request.form['stage'], request.form['valuation'], id)
    )
    db.commit()
    flash('Startup updated successfully!', 'success')
    return redirect('/startups')


# ========================================
# 7. INVESTOR VIEW WITH FILTERS
# Multi-filter system: stage, city, valuation range
# ========================================
@app.route('/investors')
def investors():
    role = session.get('role')
    
    if not role or role != 'investor':
        return redirect('/dashboard')
    
    # Get filter parameters from URL query string
    stage = request.args.get('stage', '')
    city = request.args.get('city', '')
    min_val = request.args.get('min_val', '')
    max_val = request.args.get('max_val', '')
    
    # Build dynamic SQL query with filters
    query = "SELECT * FROM Startups WHERE 1=1"
    params = []
    
    if stage:
        query += " AND stage = %s"
        params.append(stage)
    
    if city:
        query += " AND city LIKE %s"
        params.append(f'%{city}%')
    
    if min_val:
        query += " AND valuation >= %s"
        params.append(int(min_val))
    
    if max_val:
        query += " AND valuation <= %s"
        params.append(int(max_val))
    
    query += " ORDER BY name"
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    # Get unique cities for filter dropdown
    cursor.execute("SELECT DISTINCT city FROM Startups ORDER BY city")
    cities = cursor.fetchall()
    
    return render_template('investors.html', 
                      startups=data,
                      cities=cities,
                      selected_stage=stage,
                      selected_city=city,
                      min_val=min_val,
                      max_val=max_val)


# ========================================
# 8. STARTUP DETAIL VIEW
# Individual startup information page
# ========================================
@app.route('/startup/<int:id>')
def detail(id):
    role = session.get('role')
    
    if not role:
        return redirect('/')
    
    cursor.execute("SELECT * FROM Startups WHERE startup_id=%s", (id,))
    data = cursor.fetchone()
    
    if not data:
        flash('Startup not found', 'danger')
        return redirect('/startups')
    
    return render_template('detail.html', s=data, role=role)


# ========================================
# 9. LOGOUT - SESSION CLEAR
# ========================================
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect('/')


# ========================================
# 10. ADDITIONAL ROUTES (SIGNUP, PAGES)
# ========================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        stage = request.form.get('stage')
        valuation = request.form.get('valuation')
        
        if not all([name, city, stage, valuation]):
            flash('All fields are required', 'danger')
            return redirect('/signup')
        
        try:
            cursor.execute(
                "INSERT INTO Startups (name, city, stage, valuation) VALUES (%s, %s, %s, %s)",
                (name, city, stage, int(valuation))
            )
            db.commit()
            session['role'] = 'startup'
            session['startup_id'] = cursor.lastrowid
            flash('Startup registered successfully!', 'success')
            return redirect('/dashboard')
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
    
    return render_template('signup.html')


# ========================================
# MAIN EXECUTION
# Start Flask development server on port 5050
# ========================================
if __name__ == '__main__':
    app.run(debug=True, port=5050)

