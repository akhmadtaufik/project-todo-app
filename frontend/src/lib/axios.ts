import axios from 'axios';

// Environment handling
// Browser calls localhost:5000 (proxied via Next.js or direct CORS)
// Server calls web:5000 (docker network)
const baseURL = typeof window === 'undefined' 
  ? process.env.INTERNAL_API_URL 
  : process.env.NEXT_PUBLIC_API_URL;

const api = axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Inject Token
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Interceptors for auto-refresh
api.interceptors.response.use(
  (response) => {
    // Force parse if string (fix for JSDOM/MSW interaction)
    if (typeof response.data === 'string') {
      try {
        response.data = JSON.parse(response.data);
      } catch (e) {
        // failed to parse, leave as is
      }
    }
    return response;
  },
  async (error) => {
    // Parse error response if string
    if (error.response && typeof error.response.data === 'string') {
        try {
            error.response.data = JSON.parse(error.response.data)
        } catch {}
    }

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
