import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";
import { useChat } from "../context/ChatContext";

export const ChatPage: React.FC = () => {
  const { chatId } = useParams<{ chatId: string }>();
  const {
    fetchChatList,
    fetchChatMessages,
    setActiveChatId,
    clearActiveChat,
  } = useChat();

  // Load user's chat list on initial mount
  useEffect(() => {
    fetchChatList();
  }, []);

  // Synchronize route param with active chat ID and load its messages
  useEffect(() => {
    if (chatId) {
      const numericId = Number(chatId);
      if (!isNaN(numericId)) {
        fetchChatMessages(numericId);
      }
    } else {
      setActiveChatId(null);
      clearActiveChat();
    }
  }, [chatId]);

  return <MainLayout />;
};

export default ChatPage;
