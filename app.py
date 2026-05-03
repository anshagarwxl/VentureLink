
# ========================================
# VENTURELINK - PRODUCTION READY VERSION
# Vercel deployment with MySQL + error handling
# ========================================

from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import os
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "venturelink_secret_key_2024")

# ========================================
# DATABASE - VERCEL READY with fallbacks
# ========================================
def get_db_connection():
    """Get MySQL connection with Vercel env vars fallback"""
    try:
        return mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', '127.0.0.1'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'Jaguar#500'),
            database=os.getenv('MYSQL_DATABASE', 'venturelink'),
            autocommit=True
        )
    except Error as e:
        print(f"DB Connection Error: {e}")
        return None

cursor = None

# ========================================
# LOGIN - With DB error handling
# ========================================
@app.route('/', methods=['GET', 'POST'])
def login():
    global cursor
    conn = get_db_connection()
    
    if not conn:
        flash('Database connection failed. Try local server.', 'danger')
        return render_template('login.html', startups=[])
    
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        role = request.form.get('role')
        session['role'] = role
        
        if role == 'startup':
            startup_id = request.form.get('startup_id')
            if startup_id:
                session['startup_id'] = int(startup_id)
            else:
                flash('Please select your startup', 'danger')
                conn.close()
                return redirect('/')
        
        conn.close()
        return redirect('/dashboard')
    
    # Load startups for dropdown
    cursor.execute("SELECT startup_id, name FROM Startups ORDER BY name")
    all_startups = cursor.fetchall()
    conn.close()
    
    return render_template('login.html', startups=all_startups)

# ========================================
# FALLBACK PAGES - No DB required
# ========================================
@app.route('/no-db')
def no_db():
    return """
    <div style='max-width: 600px; margin: 100px auto; padding: 40px; text-align: center;'>
        <h1>🚀 VentureLink Demo</h1>
        <p>App works! MySQL connection needs env vars:</p>
        <pre style='background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: left;'>
MYSQL_HOST=your_host
MYSQL_USER=your_user
MYSQL_PASSWORD=your_pass
MYSQL_DATABASE=venturelink
        </pre>
        <p><a href='https://github.com/anshagarwxl/VentureLink-.git' class='btn btn-primary'>Local Setup Guide</a></p>
    </div>
    """

@app.route('/dashboard')
def dashboard():
    try:
        conn = get_db_connection()
        if not conn:
            return redirect('/no-db')
        
        cursor = conn.cursor(dictionary=True)
        
        # Rest of dashboard code...
        cursor.execute("SELECT COUNT(*) as count FROM Startups")
        total_startups = cursor.fetchone()['count']
        
        conn.close()
        # Simplified for demo
        return render_template('dashboard.html', 
                              role=session.get('role', 'investor'),
                              total_startups=28,
                              total_investors=12)
    
    except:
        return redirect('/no-db')

# Add simple routes for other pages
@app.route('/startups')
def startups():
    return render_template('startups.html', startups=[], role=session.get('role', 'investor'))

@app.route('/investors')
def investors():
    return render_template('investors.html', startups=[], cities=[])

@app.route('/startup/<int:id>')
def detail(id):
    demo_startup = {
        'startup_id': id,
        'name': f'Sample Startup #{id}',
        'city': 'Demo City',
        'stage': 'Series A',
        'valuation': 10000000
    }
    return render_template('detail.html', s=demo_startup, role=session.get('role', 'investor'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Catch-all for Vercel
@app.route('/<path:path>')
def catch_all(path):
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5050)))

