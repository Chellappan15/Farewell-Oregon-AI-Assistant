import React, { useState } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";
import ChatWindow from "../chat/ChatWindow";
import IntelligencePanel from "../intelligence/IntelligencePanel";
import type { Conversation, ChatMessage, ChatList } from "../../types/chat";

export interface MainLayoutProps {
  conversations?: Conversation[];
  activeConversationId: string;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  onDeleteConversation?: (id: string) => void;
  messages: ChatMessage[];
  isLoading: boolean;
  isMessagesLoading?: boolean;
  onSendMessage: (content: string) => void;
  onSelectPrompt?: (prompt: string) => void;
  onClearChat?: () => void;
  chatHistory: ChatList[];
}

export const MainLayout: React.FC<MainLayoutProps> = ({
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  messages,
  isLoading,
  isMessagesLoading = false,
  onSendMessage,
  onSelectPrompt,
  onClearChat,
  chatHistory,
}) => {
  const [sidebarMobileOpen, setSidebarMobileOpen] = useState(false);
  const [intelligenceOpen, setIntelligenceOpen] = useState(true);

  return (
    <div className="app-layout">
      {/* Sidebar - responsive desktop / mobile */}
      <Sidebar
        chatHistory={chatHistory}
        activeConversationId={activeConversationId}
        onSelectConversation={(id) => {
          onSelectConversation(id);
          setSidebarMobileOpen(false);
        }}
        onNewChat={() => {
          onNewChat();
          setSidebarMobileOpen(false);
        }}
        onDeleteConversation={onDeleteConversation}
        isOpen={sidebarMobileOpen}
        onClose={() => setSidebarMobileOpen(false)}
      />

      {/* Main Content Area */}
      <div className="main-content">
        <Header
          onToggleSidebar={() => setSidebarMobileOpen((prev) => !prev)}
          onToggleIntelligence={() => setIntelligenceOpen((prev) => !prev)}
          isIntelligenceOpen={intelligenceOpen}
          onClearChat={onClearChat}
          isMessagesLoading={isMessagesLoading}
        />

        <div className="content-area">
          <ChatWindow
            messages={messages}
            isLoading={isLoading}
            isMessagesLoading={isMessagesLoading}
            onSendMessage={onSendMessage}
            onSelectPrompt={onSelectPrompt}
          />

          <IntelligencePanel
            isOpen={intelligenceOpen}
            onClose={() => setIntelligenceOpen(false)}
          />
        </div>
      </div>
    </div>
  );
};

export default MainLayout;