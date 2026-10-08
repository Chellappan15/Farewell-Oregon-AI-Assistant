# DevMind Frontend — Gemini Build Specification

## 1. Project Context

I am building **DevMind**, an AI-powered gaming assistant for **Days Gone**.

The backend already exists and the AI pipeline is substantially complete.

### Backend / AI capabilities already implemented

- Python + FastAPI backend
- Google Gemini API using the official `google-genai` SDK
- MySQL conversation history
- ChromaDB vector database
- RAG retrieval
- Gemini receives retrieved RAG context
- Persistent conversation memory
- Function/tool calling
- Multiple tool calling
- Basic agent/tool loop
- `compare_weapons` tool
- `zombie_details` tool

The frontend must be a polished React + TypeScript application that communicates with this existing FastAPI backend.

---

# 2. Frontend Goal

Build a polished, modern **AI gaming assistant UI**, not a generic chatbot.

Product name:

**DevMind**

Subtitle:

**Gaming Intelligence**

Primary game:

**Days Gone**

The application should feel like a premium gaming/AI dashboard.

The UI should make the underlying AI architecture visible:

- RAG
- Conversation Memory
- Tool Calling
- Agent Loop
- Gemini

Do NOT make the UI look like a basic ChatGPT clone.

---

# 3. Technology Stack

Use:

- React
- TypeScript
- Vite
- CSS / Tailwind if already configured
- `lucide-react` for icons
- `framer-motion` for subtle animations
- `react-markdown` for assistant responses

Keep dependencies reasonable.

Do not introduce unnecessary libraries.

---

# 4. Existing Frontend Structure

The frontend is currently organized approximately like this:

```text
src/
│
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── MainLayout.tsx
│   │
│   ├── chat/
│   │   ├── ChatWindow.tsx
│   │   ├── MessageList.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── ChatInput.tsx
│   │   └── TypingIndicator.tsx
│   │
│   ├── intelligence/
│   │   ├── IntelligencePanel.tsx
│   │   ├── ToolActivity.tsx
│   │   ├── WeaponComparison.tsx
│   │   └── ZombieCard.tsx
│   │
│   └── common/
│       ├── IconButton.tsx
│       └── Badge.tsx
│
├── pages/
│   └── ChatPage.tsx
│
├── services/
│   └── api.ts
│
├── types/
│   └── chat.ts
│
├── App.tsx
├── main.tsx
└── index.css
```

Some files may currently be placeholders. Improve/refactor them where necessary.

---

# 5. Main Layout

The application should have three primary areas:

```text
┌─────────────────────┬────────────────────────────────┬────────────────────┐
│                     │                                │                    │
│      SIDEBAR        │           CHAT AREA            │ INTELLIGENCE PANEL │
│                     │                                │                    │
│      DevMind        │       Days Gone Assistant      │    AI Activity     │
│                     │                                │                    │
│      New Chat       │                                │    RAG             │
│      Search         │       Messages                 │    Memory          │
│                     │                                │    Tools           │
│      Recent Chats   │                                │    Agent           │
│                     │                                │                    │
│                     │                                │    Tool Results    │
│                     │                                │                    │
│      Settings       │       Chat Input               │                    │
│      User           │                                │                    │
└─────────────────────┴────────────────────────────────┴────────────────────┘
```

The layout must be responsive.

On smaller screens:

- Right intelligence panel can collapse/hide.
- Sidebar can become a drawer.
- Chat area should remain usable.

---

# 6. Visual Design

Use a dark, premium gaming/AI aesthetic.

Suggested visual direction:

- Background: very dark charcoal
- Panels: slightly lighter charcoal
- Borders: subtle gray
- Primary text: off-white
- Secondary text: muted gray
- Accent: restrained green/teal
- Avoid excessive neon colors.
- Avoid making it look like a cyberpunk template.

The design should feel:

- professional
- minimal
- technical
- gaming-oriented
- AI-focused

Use rounded corners moderately.

Use subtle shadows.

Use subtle hover transitions.

Do not over-animate the interface.

---

# 7. Sidebar

Build a polished sidebar containing:

### Header

```text
🎮 DevMind
Gaming Intelligence
```

Use a suitable Lucide icon.

### New Chat

Large button:

```text
+ New Chat
```

It should eventually create/reset the active conversation.

### Search

Search input:

```text
🔍 Search chats...
```

### Recent Chats

Display chat titles.

Example:

```text
Breaker strategy
RPD machine gun
Best weapon for hordes
How to kill Screamers
```

Use message icons.

Active chat should be visually highlighted.

### Bottom

Settings button.

User profile:

```text
Player
Survivor
```

The sidebar should eventually be prepared for dynamic chat history from the backend.

Do not hardcode the architecture in a way that makes future API integration difficult.

---

# 8. Chat Header

The header should show:

```text
Days Gone Assistant
Survival intelligence for Days Gone

● AI Online
```

Include a small status indicator.

Potential future controls:

- Clear chat
- Chat options
- Toggle intelligence panel

Use icon buttons where appropriate.

---

# 9. Chat Messages

Create reusable message components.

Message model:

```ts
export type MessageRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
}
```

The message system must support:

- User messages
- Assistant messages
- Markdown
- Code blocks if Gemini returns code
- Lists
- Bold text
- Headings
- Links where appropriate

Assistant messages should render through `react-markdown`.

User and assistant messages should have visually distinct styling.

Use avatars/icons.

---

# 10. Chat Input

Create a polished input area.

It should contain:

```text
Ask anything about Days Gone...                         ➤
```

Requirements:

- Enter sends the message.
- Shift+Enter creates a new line.
- Empty messages cannot be submitted.
- Disabled state while waiting for response.
- Send button.
- Auto-resizing textarea is preferred over a simple input.
- Show a subtle hint below:

```text
DevMind can use game knowledge, conversation memory and tools.
```

---

# 11. Loading State

Create `TypingIndicator.tsx`.

When Gemini is responding, display something like:

```text
DevMind is thinking...
● ● ●
```

Use a subtle animation.

Do not create an excessive spinner.

---

# 12. Intelligence Panel

This is one of the most important parts of the application.

The panel should make DevMind's AI architecture visible.

Title:

```text
AI Intelligence
```

Show high-level status:

```text
RAG          Ready
Memory       Ready
Tools        Ready
Agent        Ready
```

But these should eventually become dynamic.

---

# 13. AI Activity Timeline

Create:

```text
ToolActivity.tsx
```

It should display events such as:

```text
AI ACTIVITY

✓ Conversation memory loaded

✓ Retrieved 3 knowledge chunks

⚙ Calling zombie_details
  Breaker

✓ Tool completed

⚡ Gemini generating response
```

Each event should have:

- icon
- title
- optional detail
- status
- timestamp if available

Statuses:

- pending
- running
- completed
- error

Use subtle animations when a new activity appears.

---

# 14. RAG Activity

Create a visual RAG status/card.

Example:

```text
KNOWLEDGE RETRIEVAL

✓ ChromaDB

3 chunks retrieved

Top result
Breaker — Days Gone

Similarity
0.82
```

Do not expose raw internal implementation details unless useful.

The UI should communicate:

```text
Question
   ↓
Knowledge Retrieval
   ↓
Relevant Game Knowledge
```

This is important for demonstrating the project's RAG architecture.

---

# 15. Conversation Memory

Create a small memory card:

```text
CONVERSATION MEMORY

✓ Active

Previous context
5 messages

MySQL
Connected
```

The actual values should eventually come from the backend.

For now, use mock state.

---

# 16. Tool Cards

Create reusable tool-result components.

Tools currently available:

### `compare_weapons`

### `zombie_details`

Do not create generic text blobs for these.

Create specialized UI.

---

# 17. Weapon Comparison Card

Create:

```text
WeaponComparison.tsx
```

Example visual:

```text
┌─────────────────────────────────────┐
│ ⚔ Weapon Comparison                 │
│                                     │
│ SAF              MWS                │
│                                     │
│ Damage          ███████░  72        │
│ Rate of Fire    █████████ 92        │
│ Accuracy        ████████░ 84        │
│                                     │
│ AI Recommendation                   │
│ MWS is better for sustained combat. │
└─────────────────────────────────────┘
```

Important:

The frontend should NOT calculate the weapon recommendation.

The backend/tool provides structured information.

The UI only presents it.

Design the component so it can accept structured props such as:

```ts
interface WeaponComparisonData {
  first: {
    name: string;
    damage: number;
    rateOfFire: number;
    accuracy: number;
  };
  second: {
    name: string;
    damage: number;
    rateOfFire: number;
    accuracy: number;
  };
  recommendation?: string;
}
```

---

# 18. Zombie Card

Create:

```text
ZombieCard.tsx
```

Example:

```text
┌─────────────────────────────────────┐
│ ☠ BREAKER                           │
│                                     │
│ Threat: VERY HIGH                   │
│                                     │
│ Behavior                            │
│ Aggressive melee Freaker            │
│                                     │
│ Weakness                            │
│ Fire / sustained ranged attacks     │
│                                     │
│ Strategy                            │
│ Keep distance and avoid melee       │
└─────────────────────────────────────┘
```

Use structured props.

Example:

```ts
interface ZombieData {
  name: string;
  threat?: string;
  behavior?: string;
  weaknesses?: string[];
  strategy?: string;
}
```

Do not hardcode the actual game knowledge inside the component.

---

# 19. API Layer

Create:

```text
services/api.ts
```

Do NOT put fetch/axios calls directly inside UI components.

The architecture should be:

```text
ChatInput
    ↓
api.ts
    ↓
FastAPI
    ↓
RAG
    ↓
Gemini
    ↓
Tools / Agent
    ↓
FastAPI response
    ↓
api.ts
    ↓
React state
    ↓
UI
```

Create a clean API abstraction.

For example:

```ts
export async function sendMessage(
  message: string,
  chatId?: number
) {
  // call FastAPI
}
```

The exact endpoint should be configurable through an environment variable.

Use:

```text
VITE_API_BASE_URL
```

Do not hardcode:

```text
http://localhost:8000
```

throughout the application.

---

# 20. Backend Response Flexibility

The frontend must be designed so the backend can eventually return more than plain text.

Prefer a response structure conceptually similar to:

```ts
interface ChatResponse {
  message: string;

  chatId?: number;

  activities?: AIActivity[];

  rag?: {
    retrieved: boolean;
    count?: number;
    chunks?: unknown[];
  };

  toolCalls?: ToolCall[];

  toolResults?: unknown[];
}
```

Do not force the backend to immediately implement every field.

Start with the message response and make the frontend architecture extensible.

---

# 21. React State

Use React state for:

- messages
- input
- loading
- active chat
- intelligence activity
- tool results

Keep state ownership sensible.

Avoid putting the entire application's state into one giant component.

Do not introduce Redux unless there is a real need.

React Context is acceptable if it becomes useful for chat state.

---

# 22. Chat Flow

The eventual user flow should be:

```text
User types:

"How do I kill a Breaker?"

        ↓

ChatInput

        ↓

sendMessage()

        ↓

FastAPI

        ↓

Retrieve chat history

        ↓

Retrieve RAG context

        ↓

Gemini

        ↓

Gemini may call zombie_details

        ↓

Tool executes

        ↓

Agent loop

        ↓

Gemini final answer

        ↓

FastAPI response

        ↓

React

        ↓

Assistant message
+
AI activity
+
Zombie card if structured data exists
```

The UI should make this flow visible without overwhelming the user.

---

# 23. Important Existing Backend Architecture

The backend already uses:

### RAG

```text
Question
→ embedding
→ ChromaDB
→ relevant chunks
→ Gemini
```

### Memory

```text
MySQL
→ previous conversation
→ Gemini
```

### Tools

```text
Gemini
→ compare_weapons
→ zombie_details
```

### Agent loop

```text
Gemini
→ tool
→ result
→ Gemini
→ another tool if required
→ result
→ Gemini
→ final answer
```

The frontend should visually represent these capabilities.

---

# 24. Error Handling

Create a clean error state.

Examples:

```text
Unable to reach DevMind

Check that the backend is running.
```

Tool error:

```text
Tool unavailable

DevMind couldn't retrieve the requested game data.
```

Do not expose Python tracebacks to the user.

Log useful errors to the console during development.

---

# 25. Responsive Design

Desktop:

```text
Sidebar | Chat | Intelligence
```

Tablet:

```text
Sidebar | Chat
```

with Intelligence as a collapsible drawer.

Mobile:

```text
Chat
```

with Sidebar and Intelligence as drawers/sheets.

The chat must remain usable at all sizes.

---

# 26. Accessibility

Use:

- semantic HTML
- button elements for actions
- labels/aria-labels where needed
- keyboard navigation
- visible focus states
- sufficient text contrast

The chat input must be keyboard friendly.

---

# 27. Animations

Use `framer-motion` sparingly.

Good animation targets:

- Sidebar appearance
- New message
- Typing indicator
- Tool activity appearing
- Intelligence panel updates
- Cards entering the UI

Avoid:

- excessive bouncing
- huge transitions
- distracting particle effects
- constant animations

The application should feel professional.

---

# 28. Component Principles

Follow these rules:

1. One component should have one clear responsibility.
2. Avoid giant components.
3. Avoid duplicated markup.
4. Use props for reusable UI.
5. Keep API calls out of presentational components.
6. Keep types in appropriate files.
7. Keep game data out of UI components.
8. Avoid unnecessary abstractions.
9. Prefer readable code over clever code.
10. Do not create files that have no meaningful responsibility.

---

# 29. Important Development Rule

Do NOT blindly rewrite the entire project in one huge file.

Build/refactor incrementally.

First make sure:

```text
App
→ ChatPage
→ MainLayout
→ Sidebar
→ ChatWindow
→ MessageList
→ MessageBubble
→ ChatInput
→ IntelligencePanel
```

works.

Then implement:

```text
ToolActivity
WeaponComparison
ZombieCard
```

Then implement:

```text
api.ts
```

Then connect the FastAPI backend.

---

# 30. What Gemini Should Do

Act as a senior React/TypeScript engineer helping complete this project.

Build the frontend incrementally.

For every major change:

1. Explain briefly what is being changed.
2. Identify the files that will change.
3. Provide complete code for those files.
4. Explain how the pieces connect.
5. Tell me exactly how to test the change.
6. Do not move to the next major phase until the current phase is working.

Do not dump the entire project explanation at once.

Prioritize working code and clean architecture.

---

# 31. Final Product Vision

The finished application should communicate this immediately to someone viewing the GitHub project:

> "This isn't just a chatbot. This is an AI application that combines RAG, persistent conversational memory, Gemini tool calling, and an agent loop to provide context-aware gaming assistance."

The UI should reinforce that story.

Build for quality, readability, maintainability, and a strong developer portfolio presentation.
