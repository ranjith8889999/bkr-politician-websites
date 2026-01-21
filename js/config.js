/**
 * Configuration Management
 * Fetches configuration from server environment variables
 */

// Global config object
window.APP_CONFIG = {
    apiKey: null,
    environment: 'production',
    apiBaseUrl: '/api',
    loaded: false
};

/**
 * Load configuration from server
 * Call this before making any API requests
 */
async function loadConfig() {
    if (window.APP_CONFIG.loaded) {
        return window.APP_CONFIG;
    }

    try {
        const response = await fetch('/api/config');
        const result = await response.json();
        
        if (result.success) {
            window.APP_CONFIG = {
                ...window.APP_CONFIG,
                ...result.data,
                loaded: true
            };
            console.log('✅ Configuration loaded from server');
        } else {
            console.error('❌ Failed to load config:', result.error);
            // Use fallback values
            window.APP_CONFIG.loaded = true;
        }
    } catch (error) {
        console.error('❌ Error loading config:', error);
        // Use fallback values
        window.APP_CONFIG.loaded = true;
    }
    
    return window.APP_CONFIG;
}

/**
 * Get API key from loaded config
 */
function getApiKey() {
    if (!window.APP_CONFIG.loaded) {
        console.warn('⚠️ Config not loaded yet. Call loadConfig() first.');
    }
    return window.APP_CONFIG.apiKey || 'bkr-secret-key-2024';
}

/**
 * Get configuration value
 */
function getConfig(key, defaultValue = null) {
    if (!window.APP_CONFIG.loaded) {
        console.warn('⚠️ Config not loaded yet. Call loadConfig() first.');
    }
    return window.APP_CONFIG[key] || defaultValue;
}

// Auto-load config when script loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadConfig);
} else {
    loadConfig();
}
