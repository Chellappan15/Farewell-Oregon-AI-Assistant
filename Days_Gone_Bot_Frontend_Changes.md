# Frontend API Integration Task

## Objective

Modify **only the frontend folder** of the project to prepare the frontend for backend API integration.

The backend already provides the required functionality. The backend files should be used **only as reference/information** to understand the API endpoints, request payloads, response structures, and expected behavior.

### Important

**DO NOT modify anything inside the backend folder.**

---

# Scope

All changes must be limited to the **frontend folder**.

The frontend needs to be prepared for three backend operations:

1. Get chat list
2. Delete chat
3. Process/query a chat message

These API functions should be created inside the existing `services` folder.

---

# 1. Create API Service Functions

Locate the existing frontend `services` folder.

Add API service functions for the following operations.

### API 1 — Get Chat List

Create a service function responsible for retrieving the user's available chats.

Expected responsibility:

```text
Frontend → Backend
           Get chat list
           ↓
Frontend receives chat list
```

The function should:

* Call the appropriate backend endpoint.
* Use the existing frontend API configuration/pattern if one already exists.
* Match the backend's expected request format.
* Return the backend response in a frontend-friendly manner.
* Handle API errors consistently with the existing frontend conventions.

---

### API 2 — Delete Chat

Create a service function responsible for deleting a chat.

Expected responsibility:

```text
Frontend → Backend
           Delete selected chat
           ↓
Frontend receives success/error response
```

The function should:

* Call the appropriate backend endpoint.
* Accept the required chat identifier.
* Match the backend's expected request format.
* Return the backend response.
* Handle errors consistently with the existing frontend conventions.

---

### API 3 — Query Processing

Create a service function responsible for sending a user's query/message to the backend.

Expected responsibility:

```text
Frontend → Backend
           User query
           ↓
Backend processes query
           ↓
Frontend receives response
```

The function should:

* Accept the required query/message data.
* Match the backend's expected request payload.
* Call the appropriate backend endpoint.
* Return the backend response.
* Handle errors consistently with the existing frontend conventions.

---

# 2. Backend Is READ-ONLY

The backend folder must **NOT be modified**.

You may inspect backend files to determine:

* API routes
* HTTP methods
* Request payloads
* Required parameters
* Response structures
* Error responses
* Authentication requirements, if any
* Existing API conventions

Use the backend only as a source of information.

### Strict rule

```text
BACKEND FOLDER
     ↓
READ ONLY
     ↓
Use for understanding API contracts
```

Do not:

* Modify backend files.
* Rename backend files.
* Refactor backend code.
* Fix backend issues.
* Add endpoints.
* Change database code.
* Change backend models.
* Change backend configuration.

---

# 3. Create/Update Frontend Context

The API service functions should be integrated into an appropriate React Context.

The Context should become the frontend layer responsible for interacting with these services.

Conceptually:

```text
React Components
       ↓
     Context
       ↓
  API Services
       ↓
    Backend
```

The Context should be prepared to use the three service functions:

```text
getChatList()
deleteChat()
processQuery()
```

The exact function names can follow the project's existing naming conventions.

---

# 4. Hook the Context Into App.jsx

Integrate the relevant Context Provider into `App.jsx`.

The goal is to make the context available throughout the application.

Conceptually:

```jsx
<App>
   <YourContextProvider>
      <Application />
   </YourContextProvider>
</App>
```

Follow the existing project architecture and React conventions.

Do not unnecessarily restructure the application.

---

# 5. IMPORTANT — DO NOT CALL THE APIs YET

This is extremely important.

The API functions should be **implemented and wired into the Context**, but they should **NOT actually be called from the frontend yet**.

Do not:

* Call `getChatList()` automatically.
* Call `deleteChat()` from any UI.
* Call `processQuery()` from the chat UI.
* Add `useEffect()` calls that trigger the APIs.
* Add button handlers that trigger these APIs.
* Add automatic API requests on application startup.
* Add test API calls from components.
* Add mock calls intended to verify the endpoints.

The purpose of this task is only to **prepare the API integration layer**.
Use axios as http client.

---

# 6. Desired Architecture

The final frontend structure should conceptually look like:

```text
frontend/
│
├── services/
│   ├── ...
│   └── chatService.js
│
├── context/
│   ├── ...
│   └── ChatContext.jsx
│
├── components/
│   └── ...
│
├── App.jsx
└── ...
```

The exact filenames should follow the existing project's structure and naming conventions.

---

# 7. Separation of Responsibilities

Maintain a clean separation between the layers.

### Services

Responsible only for:

```text
HTTP communication
```

Example responsibility:

```text
getChatList()
deleteChat()
processQuery()
```

### Context

Responsible for:

```text
Application-level chat state
+
Exposing API operations to components
```

### Components

For this task:

```text
DO NOT invoke the API functions.
```

Components should not be changed merely to test the APIs.

---

# 8. Do Not Over-Engineer

Keep the implementation simple.

Do not introduce:

* New state-management libraries
* Redux
* React Query
* Additional architecture/frameworks
* Unnecessary abstractions
* New backend functionality

Reuse the project's existing dependencies and patterns wherever possible.

---

# 9. Existing Code Must Be Preserved

Before making changes:

1. Inspect the existing frontend structure.
2. Inspect the existing services.
3. Inspect existing contexts.
4. Inspect `App.jsx`.
5. Inspect the backend API implementation for reference.
6. Determine the correct API contracts.
7. Make the smallest changes necessary.

Do not replace working frontend code unnecessarily.

---

# 10. Final Requirements Checklist

Before finishing, verify:

* [ ] Only frontend files were modified.
* [ ] Backend files were not modified.
* [ ] Backend was used only for API contract/reference information.
* [ ] Service function for getting chat list exists.
* [ ] Service function for deleting a chat exists.
* [ ] Service function for query processing exists.
* [ ] API functions use the correct backend endpoints.
* [ ] API request payloads match the backend.
* [ ] API response handling matches the backend.
* [ ] API functions are integrated into the appropriate Context.
* [ ] Context is connected through `App.jsx`.
* [ ] No API is automatically called on application startup.
* [ ] No API is called from components.
* [ ] No UI functionality has been added to trigger these APIs.
* [ ] Existing frontend functionality remains intact.
* [ ] No unnecessary dependencies or architecture were introduced.

---

# Definition of Done

The task is complete when the frontend contains a clean API integration layer with:

```text
                 App.jsx
                    │
                    ▼
             Chat Context
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
     Get Chats   Delete Chat  Query
          │         │         │
          └─────────┼─────────┘
                    ▼
                 Backend
```

However, **none of the three API operations should actually execute yet**.

The frontend should simply be **ready for the next task**, where these functions will be connected to the actual UI behavior.
