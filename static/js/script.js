// DiabetesRisk JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // BMI Calculator
    const weightInput = document.querySelector('input[name="weight"]');
    const heightInput = document.querySelector('input[name="height"]');
    const bmiInput = document.querySelector('input[name="bmi"]');
    
    if (weightInput && heightInput && bmiInput) {
        function calculateBMI() {
            const weight = parseFloat(weightInput.value);
            const height = parseFloat(heightInput.value);
            
            if (weight && height && height > 0) {
                const bmi = weight / ((height / 100) ** 2);
                bmiInput.value = bmi.toFixed(2);
            }
        }
        
        weightInput.addEventListener('change', calculateBMI);
        heightInput.addEventListener('change', calculateBMI);
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Alert auto-close
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            // Don't auto-close for now
        }, 5000);
    });
    
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Format currency/numbers
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

// Format percentage
function formatPercentage(value) {
    return (value * 100).toFixed(2) + '%';
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
