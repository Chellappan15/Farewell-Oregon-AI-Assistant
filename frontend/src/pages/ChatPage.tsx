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
  } = useChat();

  useEffect(() => {
    fetchChatList();
  }, []);

  useEffect(() => {
    if (chatId) {
      const numericId = Number(chatId);
      if (!isNaN(numericId)) {
        fetchChatMessages(numericId);
      }
    } else {
      setActiveChatId(null);
    }
  }, [chatId]);

  return <MainLayout />;
};

export default ChatPage;
