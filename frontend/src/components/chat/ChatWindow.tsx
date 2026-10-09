import React from "react";
import MessageList from "./MessageList";
import ChatInput from "./ChatInput";
import { useChat } from "../../context/ChatContext";

export const ChatWindow: React.FC = () => {
  const { sendQuery, isQueryProcessing, isMessagesLoading } = useChat();

  return (
    <section className="chat-window-section">
      <div className="chat-window-messages">
        <MessageList />
      </div>
      <div className="chat-window-input-area">
        <ChatInput
          onSendMessage={sendQuery}
          disabled={isQueryProcessing || isMessagesLoading}
        />
      </div>
    </section>
  );
};

export default ChatWindow;