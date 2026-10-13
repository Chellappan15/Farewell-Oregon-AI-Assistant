# Implement User Authentication: Registration, Login, and JWT Sessions

## Objective

Implement a complete user authentication system with backend API endpoints for user registration and login, secure password hashing, JWT-based authentication, and a frontend authentication page.

### 1. Backend Requirements

**A. User Registration Endpoint**

Create an API endpoint to register new users.

* Accept the required user details, including email and password.
* Validate the input and ensure the email address is unique.
* Hash the password securely before storing it in the database. Never store plain-text passwords.
* Store the user's details in the existing database using the current project architecture and database conventions.
* Return an appropriate success response after successful registration.
* Handle duplicate emails, invalid inputs, and database errors appropriately.
* Never return the password or password hash in the API response.

**B. User Login Endpoint**

Create an API endpoint that authenticates users using their email and password.

* Accept the user's email and password.
* Retrieve the user record using the email address.
* Verify the submitted password against the stored password hash.
* Return an appropriate authentication error if the credentials are invalid.
* On successful authentication, generate a signed JWT containing the user's identifier and any necessary claims.
* Configure the JWT to expire after 24 hours.
* Return the JWT and the minimum user information required by the frontend.
* Use environment variables for the JWT secret and other sensitive configuration.
* Never expose the JWT secret or stored password hash in API responses.

### 2. Frontend Requirements

Create a user authentication page that supports both registration and login.

**A. Registration UI**

* Provide fields for email and password, along with any other required registration details.
* Validate inputs before submitting the form.
* Display appropriate success and error messages.
* Allow users to navigate to the login form after registration.

**B. Login UI**

* Provide email and password fields.
* Submit credentials to the backend login endpoint.
* Display clear validation and authentication error messages.
* Prevent duplicate submissions while a request is in progress.

**C. JWT Session Management**

* After a successful login, store the JWT returned by the backend in browser localStorage.
* Store the token's expiration timestamp or use its expiration claim to determine when the session expires.
* Ensure the frontend treats the session as valid for no longer than 24 hours.
* Restore the authenticated state when the page is refreshed, provided the token is still valid.
* Automatically clear the expired token and reset the authenticated state.
* Include the JWT in the Authorization header as `Bearer <token>` when calling protected backend endpoints.
* Implement a logout function that clears the stored token and resets the frontend authentication state.

### 3. Application Integration

* Integrate the authentication flow into the existing frontend application.
* Add the necessary authentication context or state management using the project's existing conventions.
* Ensure unauthenticated users are directed to the login page wherever authentication is required.
* Redirect users appropriately after successful login.
* Preserve existing application functionality and UI components.
* Reuse existing API service modules, database models, and shared utilities wherever possible.

### 4. Security and Reliability

* Use a suitable password-hashing algorithm such as Argon2id or bcrypt.
* Validate all inputs on the backend, even if frontend validation exists.
* Use generic login error messages to avoid revealing whether an email address is registered.
* Verify JWT signatures and expiration on the backend for every protected endpoint.
* Do not rely on frontend token expiration checks as a substitute for backend JWT verification.
* Never hardcode secrets or commit them to source control.
* Add appropriate error handling and tests for registration, login, invalid credentials, expired tokens, and duplicate registrations.

**Important security note:** Because localStorage is accessible to JavaScript running on the page, a successful cross-site scripting (XSS) attack can expose the JWT. Follow appropriate XSS prevention practices. If the application architecture permits, consider an HttpOnly, Secure, SameSite cookie for session storage instead.

### 5. Implementation Constraints

* Inspect the existing project structure before making changes.
* Follow the existing backend framework, frontend framework, database schema, and coding conventions.
* Do not introduce a new framework or replace existing architecture without a clear requirement.
* Make only the changes necessary to implement authentication.
* Do not break existing API endpoints or frontend functionality.
* Add or update dependencies only when required.
* Provide a summary of modified files, new endpoints, environment variables, database changes, and instructions for running and testing the implementation.

### 6. Acceptance Criteria

The implementation is complete when:

1. A new user can register successfully.
2. Passwords are stored only as secure hashes.
3. Duplicate email registrations are rejected.
4. Users can log in using valid email and password credentials.
5. Invalid credentials are rejected.
6. Successful login returns a signed JWT with a 24-hour expiration.
7. The frontend stores the JWT in localStorage and restores valid sessions after refresh.
8. Expired sessions are cleared and cannot access protected backend endpoints.
9. Logout clears the session.
10. Existing application functionality remains intact.
