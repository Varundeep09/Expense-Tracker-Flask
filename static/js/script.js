// Flash message auto-hide
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Form validation and enhancements
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(function(input) {
        if (!input.value.trim()) {
            input.style.borderColor = 'var(--danger-color)';
            isValid = false;
        } else {
            input.style.borderColor = 'var(--border)';
        }
    });
    
    return isValid;
}

// Add smooth transitions to form elements
document.querySelectorAll('input, select').forEach(function(element) {
    element.addEventListener('focus', function() {
        this.style.transform = 'scale(1.02)';
    });
    
    element.addEventListener('blur', function() {
        this.style.transform = 'scale(1)';
    });
});

// Expense form category icons
const categoryIcons = {
    'food': 'fas fa-utensils',
    'transport': 'fas fa-car',
    'entertainment': 'fas fa-film',
    'shopping': 'fas fa-shopping-bag',
    'bills': 'fas fa-file-invoice',
    'healthcare': 'fas fa-heartbeat',
    'education': 'fas fa-graduation-cap',
    'travel': 'fas fa-plane',
    'other': 'fas fa-tag'
};

// Add loading states to buttons
document.querySelectorAll('form').forEach(function(form) {
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            submitBtn.disabled = true;
        }
    });
});

// Budget preview update
function updateBudgetPreview() {
    const budgetInput = document.getElementById('monthly_budget');
    const thresholdInput = document.getElementById('alert_threshold');
    
    if (budgetInput && thresholdInput) {
        function updatePreview() {
            const budget = parseFloat(budgetInput.value) || 0;
            const threshold = parseFloat(thresholdInput.value) || 0;
            const alertAmount = (budget * threshold / 100);
            
            const alertLabel = document.querySelector('.budget-label span:last-child');
            const budgetLabel = document.querySelectorAll('.budget-label span:last-child')[1];
            const alertFill = document.querySelector('.budget-fill.budget-warning');
            
            if (alertLabel) alertLabel.textContent = `$${alertAmount.toFixed(2)}`;
            if (budgetLabel) budgetLabel.textContent = `$${budget.toFixed(2)}`;
            if (alertFill) alertFill.style.width = `${threshold}%`;
        }
        
        budgetInput.addEventListener('input', updatePreview);
        thresholdInput.addEventListener('input', updatePreview);
    }
}

// Initialize budget preview on budget page
if (document.getElementById('monthly_budget')) {
    updateBudgetPreview();
}

// Add hover effects to cards
document.querySelectorAll('.stat-card, .dashboard-card, .feature-card').forEach(function(card) {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation delays to grid items
document.querySelectorAll('.stats-grid .stat-card').forEach(function(card, index) {
    card.style.animationDelay = `${index * 100}ms`;
});

// Format number inputs on blur
document.querySelectorAll('input[type="number"]').forEach(function(input) {
    input.addEventListener('blur', function() {
        if (this.value && this.step === '0.01') {
            this.value = parseFloat(this.value).toFixed(2);
        }
    });
});

// Add ripple effect to buttons
document.querySelectorAll('.btn').forEach(function(button) {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(function() {
            ripple.remove();
        }, 600);
    });
});

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);