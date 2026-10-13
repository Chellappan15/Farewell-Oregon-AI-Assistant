import apiClient from "./api";
import type {
  User,
  AuthData,
  LoginCredentials,
  RegisterCredentials,
} from "../types/auth";
import type { ApiResponse } from "../types/chat";

// Authenticate user with email and password
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

// Register a new user
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

// Retrieve user using the token available
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
