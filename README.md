<<<<<<< HEAD

# 🚀 VentureLink - Startup Investor Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com/)

## 📖 Overview

**VentureLink** is a **full-stack web application** connecting **Startups** and **Investors** with modern UI and **role-based access control**. Built with **Flask**, **Bootstrap 5**, and **MySQL**, it provides professional dashboards, filtering, and CRUD operations.

### 🎯 Key Features

- **Role-Based Authentication** (Startup/Investor)
- **Access Control** (Startups edit only their own data)
- **Investor Filters** (Stage, City, Valuation Range)
- **Responsive Design** (Mobile-First)
- **Modern UI** (Cards, Tables, Animations)
- **Flash Messages** & Error Handling
- **Session Management**

## 🏗️ Tech Stack

```
Backend: Flask, MySQL Connector
Frontend: HTML5, Bootstrap 5, Custom CSS, JavaScript
Database: MySQL (venturelink database)
Icons: Font Awesome 6
Deployment: Ready for Heroku/Vercel
```

## 📁 Project Structure

```
venturelink_app/
├── app.py                 # Flask routes + business logic
├── static/
│   ├── style.css         # Custom styling
│   └── script.js         # Client-side JS
├── templates/            # Jinja2 templates
│   ├── base.html        # Master layout
│   ├── login.html       # Role selection
│   ├── dashboard.html   # Role-based dashboard
│   ├── startups.html    # CRUD operations
│   ├── investors.html   # Filtered investor view
│   └── detail.html      # Startup details
└── README.md            # This file!
```

## 🚀 Quick Start

### 1. Prerequisites
```bash
# MySQL (venturelink database with Startups/Investors tables)
# Python 3.8+
pip install flask mysql-connector-python
```

### 2. Clone & Run
```bash
git clone https://github.com/anshagarwxl/VentureLink-.git
cd VentureLink-
python app.py
```

### 3. Access App
```
http://localhost:5050
```

## 🎮 User Flows

### **Startup Role** 🚀
```
1. Login → Select Startup → Dashboard (Edit own data)
2. Startups Page → Edit/Add/Delete OWN startup only
3. Detail View → View startup profile
```

### **Investor Role** 💰
```
1. Login → Dashboard (Stats + Explore)
2. Investor View → Filter by Stage/City/Valuation
3. Detail View → Startup details (Read-only)
```

## 🔐 Access Control Rules

| Role | Can Edit | Can View | Can Delete | Can Filter |
|------|----------|----------|------------|------------|
| **Startup** | ✅ Own | ✅ All | ✅ Own | ❌ |
| **Investor** | ❌ | ✅ All | ❌ | ✅ All |

## 🗄️ Database Schema (Fixed - No Changes)

```sql
-- Startups Table
CREATE TABLE Startups (
    startup_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    city VARCHAR(255),
    stage VARCHAR(50),
    valuation BIGINT
);

-- Investors Table  
CREATE TABLE Investors (
    investor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    firm VARCHAR(255),
    city VARCHAR(255),
    min_invest BIGINT,
    max_invest BIGINT
);
```

## 🎨 UI Components

- **Bootstrap 5** (Grid, Cards, Tables, Modals)
- **Custom CSS** (Gradients, Hover Effects, Responsive)
- **Font Awesome** (600+ Icons)
- **Flash Messages** (Success/Error/Info)

## 📱 Responsive Breakpoints

```
Mobile: < 576px (Cards stack vertically)
Tablet: 768px (Grid layouts)
Desktop: ≥992px (Full features)
```

## 🧪 Testing

1. **Login Flow**: Startup → Select startup → Dashboard
2. **Access Control**: Try editing others → Denied
3. **Filters**: Investor → Filter by "Seed" + "Delhi" → Results
4. **Responsive**: Resize browser → Layout adapts
5. **CRUD**: Startup → Add/Edit/Delete own startup

## 📈 Sample Data Commands

```sql
-- Insert sample startups
INSERT INTO Startups (name, city, stage, valuation) VALUES 
('FinTechX', 'Delhi', 'Seed', 5000000),
('HealthAI', 'Bangalore', 'Series A', 25000000);
```

## 🔧 Development

### Environment Variables
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### Debug Mode
```bash
python app.py  # auto-reload + debug=True
```

## 🚀 Deployment

### Heroku
```bash
heroku create
heroku addons:create cleardb:ignite
git push heroku main
```

### Vercel/Netlify
Deploy `static/` + `templates/` (Flask-Proxy)

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is [MIT](LICENSE) licensed.

## 👥 Authors

**Built by BLACKBOXAI** - Professional Full-Stack Developer

---

<div align="center">
    <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
    <img src="https://img.shields.io/badge/status-production-green.svg" alt="Status">
</div>

=======
# VentureLink — Startup–Investor Platform

![License](https://img.shields.io/badge/License-MIT-yellow.svg)  
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)  
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)  
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)

## 📖 Overview

**VentureLink** is a full-stack web application designed to connect startups with investors through a clean interface and role-based system. It allows startups to manage their profiles and investors to explore, filter, and analyze startup opportunities.

## 🎯 Core Features

- 🔐 Role-Based Access (Startup / Investor)
- 🧑‍💼 Startup Management (CRUD) — Add, update, delete own data
- 🔎 Investor Filtering System — Filter by stage, city
- 📊 Dashboard Overview
- 📄 Startup Detail Pages
- 🎨 Responsive UI (Bootstrap 5)
- ⚙️ Session-Based Login (Lightweight Auth)

## 🏗️ Tech Stack

- Backend: Flask (Python)
- Frontend: HTML, Bootstrap 5, CSS, JavaScript
- Database: MySQL (venturelink)

## 👥 User Roles
- 🚀 Startup - Manage own startup details, Add/update/delete own data, View all startups
- 💰 Investor - View all startups, Apply filters (stage, city), Access startup detail pages

## 📄 License
- MIT License

## 👤 Author
- Ansh Agarwal
>>>>>>> 9cf8016f9d20f1f31ee38e83ca49f3438d1e2a7c
