/* eslint-disable react-refresh/only-export-components */
import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import type {
  User,
  LoginCredentials,
  RegisterCredentials,
  AuthContextType,
} from "../types/auth";
import * as authService from "../services/authService";

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

const STORAGE_KEY_TOKEN = "dg_auth_token";
const STORAGE_KEY_USER = "dg_auth_user";
const STORAGE_KEY_EXPIRES_AT = "dg_auth_expires_at";

export interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Initialize session from localStorage (with 24h validity check)
  useEffect(() => {
    const initializeSession = async () => {
      try {
        const storedToken = localStorage.getItem(STORAGE_KEY_TOKEN);
        const storedUser = localStorage.getItem(STORAGE_KEY_USER);
        const storedExpiresAt = localStorage.getItem(STORAGE_KEY_EXPIRES_AT);

        if (storedToken && storedExpiresAt) {
          const isExpired = new Date(storedExpiresAt).getTime() <= Date.now();

          if (isExpired) {
            // Automatically clear expired session (> 24 hours)
            localStorage.removeItem(STORAGE_KEY_TOKEN);
            localStorage.removeItem(STORAGE_KEY_USER);
            localStorage.removeItem(STORAGE_KEY_EXPIRES_AT);
            setUser(null);
            setToken(null);
          } else {
            // Restore active session
            setToken(storedToken);
            if (storedUser) {
              try {
                setUser(JSON.parse(storedUser));
              } catch {
                setUser(null);
              }
            }

            // Verify with /auth/me in background to keep user data fresh
            try {
              const freshUser = await authService.getCurrentUser();
              setUser(freshUser);
              localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(freshUser));
            } catch (err) {
              console.warn("Session verification warning:", err);
            }
          }
        }
      } catch (err) {
        console.error("Failed to restore auth session:", err);
      } finally {
        setIsLoading(false);
      }
    };

    initializeSession();
  }, []);

  const handleLogin = async (credentials: LoginCredentials): Promise<void> => {
    const authData = await authService.login(credentials);
    const expiresAt =
      authData.expiresAt ||
      new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();

    localStorage.setItem(STORAGE_KEY_TOKEN, authData.token);
    localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(authData.user));
    localStorage.setItem(STORAGE_KEY_EXPIRES_AT, expiresAt);

    setToken(authData.token);
    setUser(authData.user);
  };

  const handleRegister = async (credentials: RegisterCredentials): Promise<void> => {
    // Register
    await authService.register(credentials);

    // Automatically log in to issue JWT session
    await handleLogin({
      email: credentials.email,
      password: credentials.password,
    });
  };

  const handleLogout = (): void => {
    localStorage.removeItem(STORAGE_KEY_TOKEN);
    localStorage.removeItem(STORAGE_KEY_USER);
    localStorage.removeItem(STORAGE_KEY_EXPIRES_AT);
    setToken(null);
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!token && !!user,
    isLoading,
    login: handleLogin,
    register: handleRegister,
    logout: handleLogout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export default AuthContext;
