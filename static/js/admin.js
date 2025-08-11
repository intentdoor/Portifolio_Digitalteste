// Admin Dashboard JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize admin-specific functionality
    initializeAdminDashboard();
    setupFormValidation();
    setupFileUploadHandlers();
    setupConfirmationDialogs();
    setupDataTables();
    setupCharts();
    setupAutoSave();
});

function initializeAdminDashboard() {
    // Add loading states to admin actions
    document.querySelectorAll('.admin-action-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                this.classList.add('loading');
                this.disabled = true;
                
                // Re-enable after 3 seconds as fallback
                setTimeout(() => {
                    this.classList.remove('loading');
                    this.disabled = false;
                }, 3000);
            }
        });
    });

    // Setup real-time stats updates (placeholder for future WebSocket implementation)
    updateDashboardStats();
    
    // Auto-refresh stats every 30 seconds
    setInterval(updateDashboardStats, 30000);
}

function updateDashboardStats() {
    // In a real implementation, this would fetch updated stats from the server
    console.log('Stats updated at:', new Date().toLocaleTimeString());
}

function setupFormValidation() {
    // Enhanced form validation for admin forms
    const adminForms = document.querySelectorAll('.admin-form');
    
    adminForms.forEach(form => {
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Please fix the errors before submitting', 'danger');
            }
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        errorMessage = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} is required`;
        isValid = false;
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            errorMessage = 'Please enter a valid email address';
            isValid = false;
        }
    }
    
    // URL validation
    if (field.type === 'url' && value) {
        try {
            new URL(value);
        } catch {
            errorMessage = 'Please enter a valid URL';
            isValid = false;
        }
    }
    
    // Minimum length validation
    if (field.hasAttribute('minlength') && value.length < parseInt(field.getAttribute('minlength'))) {
        errorMessage = `Minimum ${field.getAttribute('minlength')} characters required`;
        isValid = false;
    }
    
    // Show/hide error message
    if (!isValid) {
        showFieldError(field, errorMessage);
    } else {
        clearFieldError(field);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    
    field.classList.add('is-invalid');
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function setupFileUploadHandlers() {
    // Enhanced file upload with drag-and-drop
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        const dropZone = createDropZone(input);
        
        // Drag and drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });
        
        dropZone.addEventListener('drop', handleDrop, false);
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        function highlight(e) {
            dropZone.classList.add('drag-over');
        }
        
        function unhighlight(e) {
            dropZone.classList.remove('drag-over');
        }
        
        function handleDrop(e) {
            const files = e.dataTransfer.files;
            handleFiles(files, input);
        }
        
        // Regular file input change
        input.addEventListener('change', function(e) {
            handleFiles(e.target.files, input);
        });
    });
}

function createDropZone(input) {
    const dropZone = document.createElement('div');
    dropZone.className = 'drop-zone border-2 border-dashed rounded p-4 text-center';
    dropZone.innerHTML = `
        <div class="drop-zone-content">
            <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
            <p class="mb-2">Drag and drop files here or click to browse</p>
            <small class="text-muted">Supported formats: JPG, PNG, GIF (Max 16MB)</small>
        </div>
    `;
    
    // Insert drop zone after the input
    input.style.display = 'none';
    input.parentNode.insertBefore(dropZone, input.nextSibling);
    
    // Click to trigger file input
    dropZone.addEventListener('click', () => input.click());
    
    return dropZone;
}

function handleFiles(files, input) {
    Array.from(files).forEach(file => {
        if (validateFile(file)) {
            showFilePreview(file, input);
            
            // Update the actual input
            const dt = new DataTransfer();
            dt.items.add(file);
            input.files = dt.files;
        }
    });
}

function validateFile(file) {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (!allowedTypes.includes(file.type)) {
        showToast('Please select a valid image file (JPG, PNG, GIF)', 'danger');
        return false;
    }
    
    if (file.size > maxSize) {
        showToast('File size must be less than 16MB', 'danger');
        return false;
    }
    
    return true;
}

function showFilePreview(file, input) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const dropZone = input.nextElementSibling;
        const preview = document.createElement('div');
        preview.className = 'file-preview mt-3';
        preview.innerHTML = `
            <div class="row align-items-center">
                <div class="col-auto">
                    <img src="${e.target.result}" class="img-thumbnail" style="max-width: 100px; max-height: 100px;">
                </div>
                <div class="col">
                    <h6 class="mb-1">${file.name}</h6>
                    <small class="text-muted">${formatFileSize(file.size)}</small>
                </div>
                <div class="col-auto">
                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeFilePreview(this)">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `;
        
        // Remove existing preview
        const existingPreview = dropZone.parentNode.querySelector('.file-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
        
        dropZone.parentNode.appendChild(preview);
    };
    reader.readAsDataURL(file);
}

function removeFilePreview(button) {
    const preview = button.closest('.file-preview');
    const input = preview.parentNode.querySelector('input[type="file"]');
    
    // Clear the input
    input.value = '';
    
    // Remove preview
    preview.remove();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function setupConfirmationDialogs() {
    // Enhanced confirmation dialogs for delete actions
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            const title = this.getAttribute('data-confirm-title') || 'Confirm Action';
            
            showConfirmationModal(message, title, () => {
                // If it's a form, submit it
                if (this.closest('form')) {
                    this.closest('form').submit();
                }
                // If it's a link, navigate to it
                else if (this.href) {
                    window.location.href = this.href;
                }
            });
        });
    });
}

function showConfirmationModal(message, title, onConfirm) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>${message}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger confirm-btn">Confirm</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    const bsModal = new bootstrap.Modal(modal);
    
    modal.querySelector('.confirm-btn').addEventListener('click', () => {
        onConfirm();
        bsModal.hide();
    });
    
    modal.addEventListener('hidden.bs.modal', () => {
        modal.remove();
    });
    
    bsModal.show();
}

function setupDataTables() {
    // Enhanced table functionality
    const tables = document.querySelectorAll('.admin-table');
    
    tables.forEach(table => {
        // Add sorting capability
        const headers = table.querySelectorAll('th[data-sortable]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.innerHTML += ' <i class="fas fa-sort text-muted ms-1"></i>';
            
            header.addEventListener('click', () => {
                sortTable(table, header);
            });
        });
        
        // Add search functionality if search input exists
        const searchInput = document.querySelector(`[data-table-search="${table.id}"]`);
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                filterTable(table, searchInput.value);
            });
        }
    });
}

function sortTable(table, header) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    
    // Determine sort direction
    const currentDirection = header.getAttribute('data-sort-direction') || 'asc';
    const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
    
    // Reset all headers
    table.querySelectorAll('th').forEach(th => {
        th.removeAttribute('data-sort-direction');
        const icon = th.querySelector('i');
        if (icon) {
            icon.className = 'fas fa-sort text-muted ms-1';
        }
    });
    
    // Set new direction
    header.setAttribute('data-sort-direction', newDirection);
    const icon = header.querySelector('i');
    if (icon) {
        icon.className = `fas fa-sort-${newDirection === 'asc' ? 'up' : 'down'} text-primary ms-1`;
    }
    
    // Sort rows
    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        
        // Try to parse as numbers
        const aNum = parseFloat(aText);
        const bNum = parseFloat(bText);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return newDirection === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
        // Sort as strings
        return newDirection === 'asc' 
            ? aText.localeCompare(bText)
            : bText.localeCompare(aText);
    });
    
    // Reorder DOM
    rows.forEach(row => tbody.appendChild(row));
}

function filterTable(table, query) {
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const shouldShow = text.includes(query.toLowerCase());
        row.style.display = shouldShow ? '' : 'none';
    });
}

function setupCharts() {
    // Basic chart setup (placeholder for future Chart.js integration)
    const chartContainers = document.querySelectorAll('[data-chart]');
    
    chartContainers.forEach(container => {
        const chartType = container.getAttribute('data-chart');
        // Placeholder for chart initialization
        console.log(`Chart of type ${chartType} would be initialized here`);
    });
}

function setupAutoSave() {
    // Auto-save functionality for forms
    const autoSaveForms = document.querySelectorAll('[data-autosave]');
    
    autoSaveForms.forEach(form => {
        let autoSaveTimeout;
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                clearTimeout(autoSaveTimeout);
                autoSaveTimeout = setTimeout(() => {
                    autoSaveForm(form);
                }, 2000); // Auto-save after 2 seconds of inactivity
            });
        });
    });
}

function autoSaveForm(form) {
    // In a real implementation, this would save form data to local storage or server
    console.log('Auto-saving form data...');
    
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    // Save to localStorage as fallback
    localStorage.setItem(`autosave_${form.id}`, JSON.stringify(data));
    
    // Show subtle indication of auto-save
    showAutoSaveIndicator();
}

function showAutoSaveIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'auto-save-indicator position-fixed top-0 end-0 m-3 alert alert-success alert-sm';
    indicator.innerHTML = '<i class="fas fa-check me-1"></i>Auto-saved';
    indicator.style.zIndex = '9999';
    
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.style.opacity = '0';
        setTimeout(() => {
            indicator.remove();
        }, 300);
    }, 2000);
}

// Utility functions for admin interface
window.adminUtils = {
    // Bulk actions for tables
    selectAllCheckboxes: function(masterCheckbox) {
        const checkboxes = document.querySelectorAll('.item-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = masterCheckbox.checked;
        });
        updateBulkActions();
    },
    
    // Update bulk action buttons
    updateBulkActions: function() {
        const checkedBoxes = document.querySelectorAll('.item-checkbox:checked');
        const bulkActions = document.querySelector('.bulk-actions');
        
        if (bulkActions) {
            bulkActions.style.display = checkedBoxes.length > 0 ? 'block' : 'none';
        }
    },
    
    // Export data functionality
    exportData: function(format = 'csv') {
        const table = document.querySelector('.admin-table');
        if (!table) return;
        
        const data = [];
        const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
        data.push(headers);
        
        table.querySelectorAll('tbody tr').forEach(row => {
            const rowData = Array.from(row.cells).map(cell => cell.textContent.trim());
            data.push(rowData);
        });
        
        if (format === 'csv') {
            downloadCSV(data);
        }
    }
};

function downloadCSV(data) {
    const csv = data.map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `export_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Initialize bulk action listeners
document.addEventListener('change', function(e) {
    if (e.target.classList.contains('item-checkbox')) {
        adminUtils.updateBulkActions();
    }
});

// Add CSS for admin-specific styles
const adminStyles = `
    .drop-zone {
        border-color: var(--bs-border-color) !important;
        transition: all 0.2s ease;
    }
    
    .drop-zone:hover,
    .drop-zone.drag-over {
        border-color: var(--bs-primary) !important;
        background-color: rgba(var(--bs-primary-rgb), 0.1);
    }
    
    .auto-save-indicator {
        animation: slideInFromRight 0.3s ease;
    }
    
    @keyframes slideInFromRight {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    
    .admin-table th[data-sortable] {
        user-select: none;
    }
    
    .admin-table th[data-sortable]:hover {
        background-color: rgba(var(--bs-primary-rgb), 0.1);
    }
    
    .bulk-actions {
        animation: slideDown 0.3s ease;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-10px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
`;

// Inject admin styles
if (!document.querySelector('#admin-styles')) {
    const style = document.createElement('style');
    style.id = 'admin-styles';
    style.textContent = adminStyles;
    document.head.appendChild(style);
}
