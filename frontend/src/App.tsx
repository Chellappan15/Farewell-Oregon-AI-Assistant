import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ChatProvider } from "./context/ChatContext";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <BrowserRouter>
      <ChatProvider>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/chat/:chatId" element={<ChatPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </ChatProvider>
    </BrowserRouter>
  );
}

export default App;