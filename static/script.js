// VentureLink - Custom JavaScript

// Page loaded log
window.addEventListener('DOMContentLoaded', function() {
    console.log('VentureLink Loaded 🚀');
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Button click animation
function highlightButton(btn) {
    btn.style.transform = 'scale(0.95)';
    btn.style.transition = '0.2s';
    
    setTimeout(function() {
        btn.style.transform = 'scale(1)';
    }, 150);
}

// Confirm delete function
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this startup?');
}

// Toggle startup select on login page
function toggleStartupSelect() {
    const role = document.getElementById('role').value;
    const startupSelect = document.getElementById('startupSelect');
    const startupDropdown = document.getElementById('startupSelectDropdown');
    
    if (role === 'startup') {
        startupSelect.style.display = 'block';
        startupDropdown.setAttribute('required', 'required');
    } else {
        startupSelect.style.display = 'none';
        startupDropdown.removeAttribute('required');
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Add smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Table row hover effect
const tableRows = document.querySelectorAll('tbody tr');
tableRows.forEach(function(row) {
    row.addEventListener('mouseenter', function() {
        this.style.backgroundColor = '#f9fafb';
    });
    row.addEventListener('mouseleave', function() {
        this.style.backgroundColor = '';
    });
});

// Form validation
const forms = document.querySelectorAll('.needs-validation');
forms.forEach(function(form) {
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);
});

// Logout confirmation
function confirmLogout() {
    return confirm('Are you sure you want to logout?');
}

// Add loading state to buttons
const buttons = document.querySelectorAll('.btn');
buttons.forEach(function(btn) {
    btn.addEventListener('click', function() {
        if (!this.classList.contains('no-loading')) {
            const originalText = this.innerHTML;
            this.setAttribute('data-original-text', originalText);
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
            this.classList.add('disabled');
            
            setTimeout(function() {
                btn.innerHTML = originalText;
                btn.classList.remove('disabled');
            }, 2000);
        }
    });
});

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Initialize popovers
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
});
