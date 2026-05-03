# VentureLink App - Implementation TODO

## Step 1: Update app.py
- [x] Add session validation on all routes
- [x] Add startup_id selection at login for Startup role
- [x] Add ownership check for edit/delete operations
- [x] Implement filters (stage, city, valuation) for investors route

## Step 2: Update templates/base.html
- [x] Add Bootstrap 5 CDN
- [x] Create responsive navbar with proper links
- [x] Add session-aware navigation
- [x] Include static files

## Step 3: Update templates/login.html
- [x] Add Bootstrap styling
- [x] Add role selection dropdown
- [x] Add startup selector (visible when Startup role selected)
- [x] Modern card-based UI

## Step 4: Update templates/dashboard.html
- [x] Role-based content
- [x] Startup: Show startup details + edit form
- [x] Investor: Show stats cards + explore button
- [x] Modern card UI

## Step 5: Update templates/startups.html
- [x] Add access control (edit/delete only for own startup)
- [x] Add "Add New Startup" form
- [x] Bootstrap table styling
- [x] View details button for all

## Step 6: Update templates/investors.html
- [x] Add all filters (stage, city, valuation range)
- [x] Bootstrap form styling
- [x] Table view with View Details

## Step 7: Update templates/detail.html
- [x] Card-based UI
- [x] Modern styling
- [x] Back button

## Step 8: Update static/style.css
- [x] Add custom styling
- [x] Login page styling
- [x] Dashboard styling

## Step 9: Run and Test
- [x] Test login flow with both roles
- [x] Test access control
- [x] Test filters
- [x] Verify all functionality works