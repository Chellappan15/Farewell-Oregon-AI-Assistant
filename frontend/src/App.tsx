import { ChatProvider } from "./context/ChatContext";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <ChatProvider>
      <ChatPage />
    </ChatProvider>
  );
}

export default App;