/* =============================================
   API SERVICE FOR BKR WEBSITE
   Handles all API calls to the Flask backend
   ============================================= */

// API Configuration
// Automatically detects if running locally or in production
const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

const API_CONFIG = {
    // Use relative URLs in production since Flask serves both frontend and API
    baseURL: isLocalhost 
        ? 'http://localhost:5000/api' 
        : '/api',  // Relative URL - same server serves frontend and API
    timeout: 10000,
    // API key will be loaded from server config
    get apiKey() {
        return window.APP_CONFIG && window.APP_CONFIG.apiKey 
            ? window.APP_CONFIG.apiKey 
            : 'bkr-secret-key-2024'; // Fallback only
    }
};

// =============================================
// API HELPER FUNCTIONS
// =============================================

/**
 * Make an API request
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_CONFIG.baseURL}${endpoint}`;
    
    const config = {
        method: options.method || 'GET',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    // Add API key for protected endpoints
    if (options.requiresAuth) {
        config.headers['X-API-Key'] = API_CONFIG.apiKey;
    }
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return data;
    } catch (error) {
        console.error(`API Error [${endpoint}]:`, error);
        throw error;
    }
}

/**
 * Show loading state
 */
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <tr>
                <td colspan="10" style="text-align:center; padding: 40px;">
                    <i class="fas fa-spinner fa-spin" style="font-size: 24px; color: #1e3a5f;"></i>
                    <p style="margin-top: 10px; color: #666;">Loading...</p>
                </td>
            </tr>
        `;
    }
}

/**
 * Show error message
 */
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <tr>
                <td colspan="10" style="text-align:center; padding: 40px;">
                    <i class="fas fa-exclamation-triangle" style="font-size: 24px; color: #ff6b35;"></i>
                    <p style="margin-top: 10px; color: #666;">${message}</p>
                    <button class="btn btn-primary btn-sm" onclick="location.reload()" style="margin-top: 10px;">
                        <i class="fas fa-redo"></i> Retry
                    </button>
                </td>
            </tr>
        `;
    }
}

// =============================================
// HEALTH CAMPS API
// =============================================

const HealthCampsAPI = {
    /**
     * Get all health camps
     */
    async getAll(status = null) {
        const endpoint = status ? `/health-camps?status=${status}` : '/health-camps';
        return await apiRequest(endpoint);
    },
    
    /**
     * Get upcoming health camps (date >= today)
     */
    async getUpcoming() {
        return await apiRequest('/health-camps?upcoming=true');
    },
    
    /**
     * Get a single health camp
     */
    async getById(id) {
        return await apiRequest(`/health-camps/${id}`);
    },
    
    /**
     * Create a new health camp
     */
    async create(data) {
        return await apiRequest('/health-camps', {
            method: 'POST',
            body: JSON.stringify(data),
            requiresAuth: true
        });
    },
    
    /**
     * Update a health camp
     */
    async update(id, data) {
        return await apiRequest(`/health-camps/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
            requiresAuth: true
        });
    },
    
    /**
     * Delete a health camp
     */
    async delete(id) {
        return await apiRequest(`/health-camps/${id}`, {
            method: 'DELETE',
            requiresAuth: true
        });
    }
};

// =============================================
// COMPLAINTS API
// =============================================

const ComplaintsAPI = {
    /**
     * Get all complaints
     */
    async getAll(status = null) {
        const endpoint = status ? `/complaints?status=${status}` : '/complaints';
        return await apiRequest(endpoint, { requiresAuth: true });
    },
    
    /**
     * Create a new complaint
     */
    async create(data) {
        return await apiRequest('/complaints', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    /**
     * Update complaint status
     */
    async updateStatus(id, status) {
        return await apiRequest(`/complaints/${id}/status`, {
            method: 'PATCH',
            body: JSON.stringify({ status }),
            requiresAuth: true
        });
    }
};

// =============================================
// FEEDBACK API
// =============================================

const FeedbackAPI = {
    /**
     * Get all feedback
     */
    async getAll() {
        return await apiRequest('/feedback', { requiresAuth: true });
    },
    
    /**
     * Create new feedback
     */
    async create(data) {
        return await apiRequest('/feedback', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

// =============================================
// NEWS API
// =============================================

const NewsAPI = {
    /**
     * Get all news
     */
    async getAll(status = 'published') {
        const endpoint = `/news?status=${status}`;
        return await apiRequest(endpoint);
    },
    
    /**
     * Create a new news article
     */
    async create(data) {
        return await apiRequest('/news', {
            method: 'POST',
            body: JSON.stringify(data),
            requiresAuth: true
        });
    },
    
    /**
     * Update a news article
     */
    async update(id, data) {
        return await apiRequest(`/news/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
            requiresAuth: true
        });
    },
    
    /**
     * Delete a news article
     */
    async delete(id) {
        return await apiRequest(`/news/${id}`, {
            method: 'DELETE',
            requiresAuth: true
        });
    }
};

// =============================================
// DASHBOARD API
// =============================================

const DashboardAPI = {
    /**
     * Get dashboard statistics
     */
    async getStats() {
        return await apiRequest('/dashboard/stats', { requiresAuth: true });
    }
};

// =============================================
// HEALTH CHECK
// =============================================

/**
 * Check if API is available
 */
async function checkAPIHealth() {
    try {
        const response = await apiRequest('/health');
        console.log('✓ API Server:', response.message);
        return true;
    } catch (error) {
        console.error('✗ API Server is not responding:', error.message);
        return false;
    }
}

// =============================================
// EXPORT API MODULES
// =============================================

window.HealthCampsAPI = HealthCampsAPI;
window.ComplaintsAPI = ComplaintsAPI;
window.FeedbackAPI = FeedbackAPI;
window.NewsAPI = NewsAPI;
window.DashboardAPI = DashboardAPI;
window.checkAPIHealth = checkAPIHealth;
window.showLoading = showLoading;
window.showError = showError;
