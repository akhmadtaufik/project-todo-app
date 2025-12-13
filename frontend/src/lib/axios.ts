import axios from 'axios';

// Environment handling
// Browser calls localhost:5000 (proxied via Next.js or direct CORS)
// Server calls web:5000 (docker network)
const baseURL = typeof window === 'undefined' 
  ? (process.env.API_URL || 'http://web:5000') 
  : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000');

const api = axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptors for auto-refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Check if error is 401 and we haven't tried refreshing yet
    // Skip refresh for auth endpoints to avoid loops
    if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url?.includes('/auth/')) {
      originalRequest._retry = true;
      
      try {
        // Attempt refresh
        await api.post('/api/auth/refresh');
        
        // Retry original request
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed (token expired or invalid)
        if (typeof window !== 'undefined') {
             // Optional: Handle logout
             // window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
