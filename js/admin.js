/* =============================================
   ADMIN PANEL JAVASCRIPT
   ============================================= */

document.addEventListener('DOMContentLoaded', function() {
    initAdminPanel();
});

function initAdminPanel() {
    initSidebar();
    initTabs();
    initImageUpload();
    initModal();
    initForms();
    initDataTables();
    loadDashboardData();
}

// =============================================
// SIDEBAR TOGGLE
// =============================================
function initSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.admin-sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
}

// =============================================
// TABS
// =============================================
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            const tabContainer = this.closest('.admin-card');
            
            // Remove active from all tabs
            tabContainer.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            tabContainer.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Add active to clicked tab
            this.classList.add('active');
            tabContainer.querySelector(`#${tabId}`).classList.add('active');
        });
    });
}

// =============================================
// IMAGE UPLOAD
// =============================================
function initImageUpload() {
    const uploadAreas = document.querySelectorAll('.image-upload-area');
    
    uploadAreas.forEach(area => {
        const input = area.querySelector('input[type="file"]');
        const preview = area.parentElement.querySelector('.image-preview');
        
        area.addEventListener('click', () => input?.click());
        
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });
        
        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            handleFiles(e.dataTransfer.files, preview);
        });
        
        input?.addEventListener('change', (e) => {
            handleFiles(e.target.files, preview);
        });
    });
}

function handleFiles(files, preview) {
    if (!preview) return;
    
    Array.from(files).forEach(file => {
        if (!file.type.startsWith('image/')) return;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.innerHTML = `
                <img src="${e.target.result}" alt="Preview">
                <button class="remove-btn" onclick="this.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            `;
            preview.appendChild(previewItem);
        };
        reader.readAsDataURL(file);
    });
}

// =============================================
// MODAL
// =============================================
function initModal() {
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modalCloses = document.querySelectorAll('.modal-close, .modal-cancel');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal');
            openModal(modalId);
        });
    });
    
    modalCloses.forEach(close => {
        close.addEventListener('click', function() {
            const modal = this.closest('.modal-overlay');
            closeModal(modal);
        });
    });
    
    // Close on overlay click
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal(this);
            }
        });
    });
}

function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modal) {
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// =============================================
// FORMS
// =============================================
function initForms() {
    // Health Camp Form
    const healthCampForm = document.getElementById('healthCampForm');
    if (healthCampForm) {
        healthCampForm.addEventListener('submit', handleHealthCampSubmit);
    }
    
    // Gallery Form
    const galleryForm = document.getElementById('galleryForm');
    if (galleryForm) {
        galleryForm.addEventListener('submit', handleGallerySubmit);
    }
    
    // News Form
    const newsForm = document.getElementById('newsForm');
    if (newsForm) {
        newsForm.addEventListener('submit', handleNewsSubmit);
    }
    
    // Content Form
    const contentForm = document.getElementById('contentForm');
    if (contentForm) {
        contentForm.addEventListener('submit', handleContentSubmit);
    }
}

async function handleHealthCampSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Add default status if not provided
    if (!data.status) {
        data.status = 'upcoming';
    }
    
    try {
        // Call API to create health camp
        const response = await HealthCampsAPI.create(data);
        
        if (response.success) {
            showNotification('Health camp added successfully!', 'success');
            e.target.reset();
            closeModal(e.target.closest('.modal-overlay'));
            loadHealthCamps();
        } else {
            showNotification(response.error || 'Failed to add health camp', 'error');
        }
    } catch (error) {
        console.error('Error creating health camp:', error);
        showNotification('Error: ' + error.message, 'error');
    }
}

function handleGallerySubmit(e) {
    e.preventDefault();
    showNotification('Gallery images uploaded successfully!', 'success');
    e.target.reset();
}

function handleNewsSubmit(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    const news = JSON.parse(localStorage.getItem('newsUpdates') || '[]');
    
    news.push({
        id: Date.now(),
        ...data,
        date: new Date().toLocaleDateString()
    });
    
    localStorage.setItem('newsUpdates', JSON.stringify(news));
    
    showNotification('News article added successfully!', 'success');
    e.target.reset();
    closeModal(e.target.closest('.modal-overlay'));
    loadNewsUpdates();
}

function handleContentSubmit(e) {
    e.preventDefault();
    showNotification('Content updated successfully!', 'success');
}

// =============================================
// DATA TABLES
// =============================================
function initDataTables() {
    loadHealthCamps();
    loadComplaints();
    loadFeedback();
}

async function loadHealthCamps() {
    const container = document.getElementById('healthCampsTable');
    if (!container) return;
    
    // Show loading state
    showLoading('healthCampsTable');
    
    try {
        // Fetch camps from API
        const response = await HealthCampsAPI.getAll();
        
        if (response.success) {
            const camps = response.data;
            
            if (camps.length === 0) {
                container.innerHTML = '<tr><td colspan="6" style="text-align:center;">No health camps found. Add a new camp to get started.</td></tr>';
                return;
            }
            
            container.innerHTML = camps.map(camp => `
                <tr>
                    <td><strong>${camp.title || 'N/A'}</strong></td>
                    <td>${camp.date || 'N/A'}</td>
                    <td>${camp.location || 'N/A'}</td>
                    <td>${camp.time || 'N/A'}</td>
                    <td><span class="badge badge-${camp.status === 'upcoming' ? 'success' : 'info'}">${camp.status || 'upcoming'}</span></td>
                    <td class="actions">
                        <button class="btn btn-sm btn-primary" onclick="editCamp(${camp.id})" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteCamp(${camp.id})" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        } else {
            showError('healthCampsTable', response.error || 'Failed to load health camps');
        }
    } catch (error) {
        console.error('Error loading health camps:', error);
        showError('healthCampsTable', 'Unable to connect to server. Please check if the API is running.');
    }
}

async function deleteCamp(id) {
    if (!confirm('Are you sure you want to delete this health camp?')) return;
    
    try {
        const response = await HealthCampsAPI.delete(id);
        
        if (response.success) {
            showNotification('Health camp deleted successfully!', 'success');
            loadHealthCamps();
        } else {
            showNotification(response.error || 'Failed to delete health camp', 'error');
        }
    } catch (error) {
        console.error('Error deleting health camp:', error);
        showNotification('Error: ' + error.message, 'error');
    }
}

function loadComplaints() {
    const container = document.getElementById('complaintsTable');
    if (!container) return;
    
    const complaints = JSON.parse(localStorage.getItem('complaints') || '[]');
    
    if (complaints.length === 0) {
        container.innerHTML = '<tr><td colspan="6" style="text-align:center;">No complaints found</td></tr>';
        return;
    }
    
    container.innerHTML = complaints.map(complaint => `
        <tr>
            <td>#${complaint.id}</td>
            <td>${complaint.name || 'Anonymous'}</td>
            <td>${complaint.subject || 'N/A'}</td>
            <td>${complaint.date || 'N/A'}</td>
            <td><span class="badge badge-${getStatusBadge(complaint.status)}">${complaint.status || 'pending'}</span></td>
            <td class="actions">
                <button class="btn btn-sm btn-primary" onclick="viewComplaint(${complaint.id})"><i class="fas fa-eye"></i></button>
                <button class="btn btn-sm btn-success" onclick="resolveComplaint(${complaint.id})"><i class="fas fa-check"></i></button>
            </td>
        </tr>
    `).join('');
}

function loadFeedback() {
    const container = document.getElementById('feedbackTable');
    if (!container) return;
    
    const feedback = JSON.parse(localStorage.getItem('feedback') || '[]');
    
    if (feedback.length === 0) {
        container.innerHTML = '<tr><td colspan="5" style="text-align:center;">No feedback found</td></tr>';
        return;
    }
    
    container.innerHTML = feedback.map(item => `
        <tr>
            <td>#${item.id}</td>
            <td>${item.name || 'Anonymous'}</td>
            <td>${item.rating || 'N/A'}</td>
            <td>${item.date || 'N/A'}</td>
            <td class="actions">
                <button class="btn btn-sm btn-primary" onclick="viewFeedback(${item.id})"><i class="fas fa-eye"></i></button>
            </td>
        </tr>
    `).join('');
}

function getStatusBadge(status) {
    const badges = {
        'pending': 'warning',
        'in-progress': 'info',
        'resolved': 'success',
        'closed': 'danger'
    };
    return badges[status] || 'warning';
}

// =============================================
// DASHBOARD DATA
// =============================================
async function loadDashboardData() {
    try {
        // Try to load from API first
        const response = await DashboardAPI.getStats();
        
        if (response.success) {
            const stats = response.data;
            updateStat('totalComplaints', stats.total_complaints || 0);
            updateStat('totalFeedback', stats.total_feedback || 0);
            updateStat('totalCamps', stats.total_camps || 0);
            updateStat('pendingComplaints', stats.pending_complaints || 0);
        }
    } catch (error) {
        console.warn('Could not load stats from API, using localStorage fallback:', error);
        // Fallback to localStorage if API is not available
        const complaints = JSON.parse(localStorage.getItem('complaints') || '[]');
        const feedback = JSON.parse(localStorage.getItem('feedback') || '[]');
        const healthCamps = JSON.parse(localStorage.getItem('healthCamps') || '[]');
        
        updateStat('totalComplaints', complaints.length);
        updateStat('totalFeedback', feedback.length);
        updateStat('totalCamps', healthCamps.length);
        updateStat('pendingComplaints', complaints.filter(c => c.status === 'pending').length);
    }
}

function updateStat(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

// =============================================
// NOTIFICATION
// =============================================
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// =============================================
// AUTH FUNCTIONS
// =============================================
function checkAuth() {
    const isLoggedIn = localStorage.getItem('adminLoggedIn');
    if (!isLoggedIn && !window.location.pathname.includes('login.html')) {
        window.location.href = 'login.html';
    }
}

function login(username, password) {
    // Simple authentication - in production, use proper backend auth
    if (username === 'admin' && password === 'admin123') {
        localStorage.setItem('adminLoggedIn', 'true');
        localStorage.setItem('adminUser', username);
        return true;
    }
    return false;
}

function logout() {
    localStorage.removeItem('adminLoggedIn');
    localStorage.removeItem('adminUser');
    window.location.href = 'login.html';
}

// =============================================
// EXPORT FUNCTIONS
// =============================================
window.openModal = openModal;
window.closeModal = closeModal;
window.deleteCamp = deleteCamp;
window.showNotification = showNotification;
window.login = login;
window.logout = logout;
