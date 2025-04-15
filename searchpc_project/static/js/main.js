document.addEventListener('DOMContentLoaded', function() {
    // Form submission loading indicator
    const forms = document.querySelectorAll('form');
    const spinnerOverlay = document.getElementById('spinner-overlay');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Only show spinner for search form, not for login/signup
            if (this.querySelector('button[type="submit"]').innerText.includes('Find PC Parts')) {
                spinnerOverlay.classList.add('show');
                
                // Basic form validation
                const budgetInput = this.querySelector('#id_budget');
                const purposeSelect = this.querySelector('#id_purpose');
                const locationInput = this.querySelector('#id_location');
                
                if (budgetInput && !budgetInput.value) {
                    e.preventDefault();
                    spinnerOverlay.classList.remove('show');
                    showToast('Please enter your budget');
                    budgetInput.focus();
                    return false;
                }
                
                if (locationInput && !locationInput.value.trim()) {
                    e.preventDefault();
                    spinnerOverlay.classList.remove('show');
                    showToast('Please enter your location');
                    locationInput.focus();
                    return false;
                }
            }
        });
    });
    
    // Budget range value display
    const budgetInput = document.getElementById('id_budget');
    const budgetDisplay = document.getElementById('budget-display');
    
    if (budgetInput && budgetDisplay) {
        budgetInput.addEventListener('input', function() {
            budgetDisplay.textContent = Number(this.value).toLocaleString() + ' INR';
        });
        // Initialize display
        if (budgetInput.value) {
            budgetDisplay.textContent = Number(budgetInput.value).toLocaleString() + ' INR';
        }
    }
    
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => 
            new bootstrap.Tooltip(tooltipTriggerEl));
    }

    // Auto-expand first accordion item on results page
    const firstAccordionButton = document.querySelector('.accordion-button');
    const firstAccordionCollapse = document.querySelector('.accordion-collapse');
    
    if (firstAccordionButton && firstAccordionCollapse && 
        typeof bootstrap !== 'undefined' && 
        !firstAccordionButton.classList.contains('collapsed')) {
        const bsCollapse = new bootstrap.Collapse(firstAccordionCollapse, {
            toggle: true
        });
    }
    
    // Add toast notification functionality
    function showToast(message, type = 'danger') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            // Create toast container if it doesn't exist
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
        
        const toastId = 'toast-' + Date.now();
        const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${type === 'danger' ? 'exclamation-circle' : 'check-circle'} me-2"></i> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
        `;
        
        document.getElementById('toast-container').insertAdjacentHTML('beforeend', toastHTML);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            delay: 5000
        });
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            toastElement.remove();
        });
    }
});
