import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

// Request interceptor: Attach JWT Bearer token if valid session exists
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("dg_auth_token");
    const expiresAt = localStorage.getItem("dg_auth_expires_at");

    if (token) {
      // Check 24-hour expiration validity
      if (expiresAt && new Date(expiresAt).getTime() <= Date.now()) {
        localStorage.removeItem("dg_auth_token");
        localStorage.removeItem("dg_auth_user");
        localStorage.removeItem("dg_auth_expires_at");
      } else {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor: Handle 401 Unauthorized globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const originalRequest = error.config;
    const isAuthRoute =
      originalRequest?.url?.includes("/auth/login") ||
      originalRequest?.url?.includes("/auth/register");

    if (error.response?.status === 401 && !isAuthRoute) {
      localStorage.removeItem("dg_auth_token");
      localStorage.removeItem("dg_auth_user");
      localStorage.removeItem("dg_auth_expires_at");

      // Redirect to login if not already on login or register page
      if (
        typeof window !== "undefined" &&
        !window.location.pathname.startsWith("/login") &&
        !window.location.pathname.startsWith("/register")
      ) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
