import apiClient from "./api";
import type {
  User,
  AuthData,
  LoginCredentials,
  RegisterCredentials,
} from "../types/auth";
import type { ApiResponse } from "../types/chat";

/**
 * 1. Authenticates a user with email and password.
 * Issues a 24-hour signed JWT.
 * Endpoint: POST /auth/login
 */
export async function login(credentials: LoginCredentials): Promise<AuthData> {
  const response = await apiClient.post<ApiResponse<AuthData>>("/auth/login", {
    email: credentials.email.trim().toLowerCase(),
    password: credentials.password,
  });

  if (!response.data.data) {
    throw new Error(response.data.message || "Failed to authenticate.");
  }

  return response.data.data;
}

/**
 * 2. Registers a new survivor account.
 * Endpoint: POST /auth/register
 */
export async function register(credentials: RegisterCredentials): Promise<User> {
  const response = await apiClient.post<ApiResponse<User>>("/auth/register", {
    email: credentials.email.trim().toLowerCase(),
    password: credentials.password,
    name: credentials.name?.trim() || undefined,
  });

  if (!response.data.data) {
    throw new Error(response.data.message || "Failed to register.");
  }

  return response.data.data;
}

/**
 * 3. Retrieves the authenticated user profile using the current JWT token.
 * Endpoint: GET /auth/me
 */
export async function getCurrentUser(): Promise<User> {
  const response = await apiClient.get<ApiResponse<User>>("/auth/me");

  if (!response.data.data) {
    throw new Error(response.data.message || "Failed to fetch user profile.");
  }

  return response.data.data;
}

export default {
  login,
  register,
  getCurrentUser,
};
