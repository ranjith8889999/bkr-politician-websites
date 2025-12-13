/* =============================================
   PRODUCTION API CONFIGURATION
   Copy this content to js/api-service.js before deploying
   ============================================= */

// API Configuration for PRODUCTION
const API_CONFIG = {
    baseURL: 'https://YOUR-BACKEND-URL.com/api',  // ← UPDATE THIS with your EasyPanel backend URL
    apiKey: 'YOUR_PRODUCTION_API_KEY_HERE',       // ← UPDATE THIS to match backend/.env API_KEY
    timeout: 10000
};

/* 
IMPORTANT STEPS BEFORE DEPLOYING:
1. Get your backend URL from EasyPanel (e.g., https://bkr-backend.yourdomain.com)
2. Update baseURL above with: 'https://bkr-backend.yourdomain.com/api'
3. Update apiKey to match the API_KEY you set in backend environment variables
4. Replace the API_CONFIG section in js/api-service.js with the above
5. Upload to Hostinger

Example:
const API_CONFIG = {
    baseURL: 'https://bkr-backend.mysite.com/api',
    apiKey: 'abc123xyz789_your_secret_key_here',
    timeout: 10000
};
*/
