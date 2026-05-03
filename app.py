from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "venturelink_secret_key_2024"

# Database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Jaguar#500",
    database="venturelink"
)
cursor = db.cursor(dictionary=True)


# 🔐 Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        session['role'] = role
        
        if role == 'startup':
            startup_id = request.form.get('startup_id')
            if startup_id:
                session['startup_id'] = int(startup_id)
            else:
                flash('Please select your startup', 'danger')
                return redirect('/')
        
        return redirect('/dashboard')
    
    cursor.execute("SELECT startup_id, name FROM Startups ORDER BY name")
    all_startups = cursor.fetchall()
    return render_template('login.html', startups=all_startups)


# 🔷 Dashboard
@app.route('/dashboard')
def dashboard():
    role = session.get('role')
    
    if not role:
        return redirect('/')
    
    # Get counts
    cursor.execute("SELECT COUNT(*) as count FROM Startups")
    total_startups = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM Investors")
    total_investors = cursor.fetchone()['count']
    
    # Get featured startups for investor
    cursor.execute("SELECT * FROM Startups ORDER BY RAND() LIMIT 3")
    featured_startups = cursor.fetchall()
    
    # Get startup details for startup role
    my_startup = None
    if role == 'startup':
        startup_id = session.get('startup_id')
        if startup_id:
            cursor.execute("SELECT * FROM Startups WHERE startup_id = %s", (startup_id,))
            my_startup = cursor.fetchone()
    
    cursor.execute("SELECT startup_id, name FROM Startups ORDER BY name")
    all_startups = cursor.fetchall()
    
    return render_template('dashboard.html',
                      role=role,
                      total_startups=total_startups,
                      total_investors=total_investors,
                      my_startup=my_startup,
                      all_startups=all_startups,
                      startups=featured_startups)


# 🔷 Startups page
@app.route('/startups')
def startups():
    role = session.get('role')
    
    if not role:
        return redirect('/')
    
    cursor.execute("SELECT * FROM Startups ORDER BY name")
    data = cursor.fetchall()
    
    return render_template('startups.html', startups=data, role=role)


# 🔷 Add startup
@app.route('/add', methods=['POST'])
def add():
    role = session.get('role')
    
    if role != 'startup':
        flash('Access denied', 'danger')
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
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect('/startups')


# 🔷 Delete startup
@app.route('/delete/<int:id>')
def delete(id):
    role = session.get('role')
    
    if role != 'startup':
        flash('Access denied', 'danger')
        return redirect('/startups')
    
    startup_id = session.get('startup_id')
    
    if startup_id != id:
        flash('You can only delete your own startup', 'danger')
        return redirect('/startups')
    
    cursor.execute("DELETE FROM Startups WHERE startup_id=%s", (id,))
    db.commit()
    flash('Startup deleted!', 'success')
    return redirect('/startups')


# 🔷 Update startup
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    role = session.get('role')
    
    if role != 'startup':
        flash('Access denied', 'danger')
        return redirect('/startups')
    
    startup_id = session.get('startup_id')
    
    if startup_id != id:
        flash('You can only edit your own startup', 'danger')
        return redirect('/startups')
    
    cursor.execute(
        "UPDATE Startups SET name=%s, city=%s, stage=%s, valuation=%s WHERE startup_id=%s",
        (request.form['name'], request.form['city'],
         request.form['stage'], request.form['valuation'], id)
    )
    db.commit()
    flash('Startup updated!', 'success')
    return redirect('/startups')


# 🔷 Investor View
@app.route('/investors')
def investors():
    role = session.get('role')
    
    if not role or role != 'investor':
        return redirect('/dashboard')
    
    stage = request.args.get('stage', '')
    city = request.args.get('city', '')
    min_val = request.args.get('min_val', '')
    max_val = request.args.get('max_val', '')
    
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
    
    cursor.execute("SELECT DISTINCT city FROM Startups ORDER BY city")
    cities = cursor.fetchall()
    
    return render_template('investors.html', 
                      startups=data,
                      cities=cities,
                      selected_stage=stage,
                      selected_city=city,
                      min_val=min_val,
                      max_val=max_val)


# 🔷 Detail Page
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


# 🔷 Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out!', 'success')
    return redirect('/')


# 🔷 Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        stage = request.form.get('stage')
        valuation = request.form.get('valuation')
        
        if not name or not city or not stage or not valuation:
            flash('All fields required', 'danger')
            return redirect('/signup')
        
        try:
            cursor.execute(
                "INSERT INTO Startups (name, city, stage, valuation) VALUES (%s, %s, %s, %s)",
                (name, city, stage, int(valuation))
            )
            db.commit()
            startup_id = cursor.lastrowid
            session['role'] = 'startup'
            session['startup_id'] = startup_id
            flash('Registered successfully!', 'success')
            return redirect('/dashboard')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('signup.html')


# 🔷 Signup Investor
@app.route('/signup_investor', methods=['GET', 'POST'])
def signup_investor():
    if request.method == 'POST':
        name = request.form.get('name')
        firm = request.form.get('firm')
        city = request.form.get('city')
        min_invest = request.form.get('min_invest')
        max_invest = request.form.get('max_invest')
        
        if not name or not firm or not city or not min_invest or not max_invest:
            flash('All fields required', 'danger')
            return redirect('/signup_investor')
        
        try:
            cursor.execute(
                "INSERT INTO Investors (name, firm, city, min_invest, max_invest) VALUES (%s, %s, %s, %s, %s)",
                (name, firm, city, int(min_invest), int(max_invest))
            )
            db.commit()
            investor_id = cursor.lastrowid
            session['role'] = 'investor'
            session['investor_id'] = investor_id
            flash('Registered successfully!', 'success')
            return redirect('/dashboard')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('signup_investor.html')


# 🔷 Home page
@app.route('/home')
def home():
    return render_template('home.html')


# 🔷 About page
@app.route('/about')
def about():
    return render_template('about.html')


# 🔷 Contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you! We will get back to you soon.', 'success')
        return redirect('/contact')
    
    return render_template('contact.html')


# 🔷 Privacy page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


# 🔷 Terms page
@app.route('/terms')
def terms():
    return render_template('terms.html')


# 🔷 Saved Startups
@app.route('/saved')
def saved():
    role = session.get('role')
    
    if not role or role != 'investor':
        return redirect('/dashboard')
    
    cursor.execute("SELECT * FROM Startups ORDER BY RAND() LIMIT 5")
    data = cursor.fetchall()
    
    return render_template('saved.html', startups=data)


# 🔷 Messages
@app.route('/messages')
def messages():
    role = session.get('role')
    
    if not role:
        return redirect('/')
    
    demo_messages = [
        {'from': 'Venture Capital Partners', 'subject': 'Interested in your startup', 'time': '2 hours ago'},
        {'from': 'Angel Investor Group', 'subject': 'Request for meeting', 'time': 'Yesterday'},
        {'from': 'Tech Incubator', 'subject': 'Accelerator invitation', 'time': '2 days ago'},
    ]
    
    return render_template('messages.html', messages=demo_messages, role=role)


# 🔷 Active Deals
@app.route('/deals')
def deals():
    role = session.get('role')
    
    if not role or role != 'investor':
        return redirect('/dashboard')
    
    cursor.execute("SELECT * FROM Startups ORDER BY valuation DESC")
    data = cursor.fetchall()
    
    return render_template('deals.html', startups=data)


# 🔷 Analytics
@app.route('/analytics')
def analytics():
    role = session.get('role')
    
    if not role:
        return redirect('/')
    
    # Get startup analytics if startup
    startup_id = session.get('startup_id')
    my_startup = None
    investor_count = 0
    
    if role == 'startup' and startup_id:
        cursor.execute("SELECT * FROM Startups WHERE startup_id = %s", (startup_id,))
        my_startup = cursor.fetchone()
        
        # Count investors who showed interest (mock data)
        investor_count = 12
        
        # Mock analytics data
        views_data = [45, 52, 38, 65, 48, 72, 58, 85, 62, 78, 95, 88]
        invest_data = [2, 3, 1, 4, 2, 5, 3, 6, 4, 5, 7, 6]
    
    # Get global stats for investor
    total_startups = 0
    total_investors = 0
    avg_valuation = 0
    
    if role == 'investor':
        cursor.execute("SELECT COUNT(*) as count FROM Startups")
        total_startups = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM Investors")
        total_investors = cursor.fetchone()['count']
        
        cursor.execute("SELECT AVG(valuation) as avg FROM Startups")
        avg_valuation = cursor.fetchone()['avg'] or 0
    
    return render_template('analytics.html', 
                      role=role,
                      my_startup=my_startup,
                      investor_count=investor_count,
                      total_startups=total_startups,
                      total_investors=total_investors,
                      avg_valuation=int(avg_valuation))


# 🔷 Startup Messages (for startup role)
@app.route('/startup_messages')
def startup_messages():
    role = session.get('role')
    
    if not role or role != 'startup':
        return redirect('/dashboard')
    
    # Mock messages for startup
    demo_messages = [
        {'from': 'Sequoia Capital', 'subject': 'Interested in Series B', 'time': '2 hours ago'},
        {'from': 'Y Combinator', 'subject': 'Application status', 'time': 'Yesterday'},
        {'from': 'Tiger Global', 'subject': 'Meeting request', 'time': '3 days ago'},
    ]
    
    return render_template('startup_messages.html', messages=demo_messages)


# 🔷 Startup Documents (for startup role)
@app.route('/documents')
def documents():
    role = session.get('role')
    
    if not role or role != 'startup':
        return redirect('/dashboard')
    
# Mock documents
    docs = [
        {'name': 'Pitch Deck 2024.pdf', 'size': '2.4 MB', 'date': 'May 1, 2024'},
        {'name': 'Business Plan.pdf', 'size': '1.8 MB', 'date': 'Apr 15, 2024'},
        {'name': 'Financials.xlsx', 'size': '540 KB', 'date': 'Apr 20, 2024'},
    ]
    
    return render_template('documents.html', documents=docs)


if __name__ == '__main__':
    app.run(debug=True, port=5050)
