import React, { useState } from "react";
import {
  Gamepad2,
  Plus,
  Search,
  MessageSquare,
  Settings,
  User,
  X,
  Trash2,
} from "lucide-react";
import type { ChatList } from "../../types/chat";
import IconButton from "../common/IconButton";

export interface SidebarProps {
  chatHistory: ChatList[];
  activeConversationId: string;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  onDeleteConversation?: (id: string) => void;
  isOpen?: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  chatHistory,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  isOpen = true,
  onClose,
}) => {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredConversations = chatHistory.filter((c) =>
    c.chat_title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <>
      {/* Mobile backdrop */}
      <div
        className={`sidebar-backdrop ${isOpen ? "open" : ""}`}
        onClick={onClose}
        aria-hidden="true"
      />

      <aside className={`sidebar ${isOpen ? "open" : ""}`}>
        {/* Logo / Brand Header */}
        <div className="sidebar-logo">
          <div className="logo-icon">
            <Gamepad2 size={22} className="logo-gamepad" />
          </div>

          <div className="logo-text">
            <h2>Farewell Oregon AI</h2>
            <span>Gaming Intelligence</span>
          </div>

          {onClose && (
            <IconButton
              icon={<X size={18} />}
              label="Close Sidebar"
              size="sm"
              onClick={onClose}
              className="sidebar-close-mobile"
            />
          )}
        </div>

        {/* New Chat Button */}
        <button
          type="button"
          className="new-chat-button"
          onClick={onNewChat}
        >
          <Plus size={18} />
          <span>New Chat</span>
        </button>

        {/* Search */}
        <div className="chat-search">
          <Search size={16} className="search-icon" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search chats..."
            aria-label="Search chats"
          />
          {searchQuery && (
            <button
              type="button"
              className="search-clear-btn"
              onClick={() => setSearchQuery("")}
            >
              <X size={13} />
            </button>
          )}
        </div>

        {/* Recent Chats Section */}
        <div className="recent-section">
          <p className="section-title">RECENT CONVERSATIONS</p>

          <div className="recent-list">
            {filteredConversations.length > 0 ? (
              filteredConversations.map((conv) => {
                const isActive = String(conv.chat_id) === activeConversationId;
                return (
                  <div
                    key={conv.id}
                    className={`chat-item ${isActive ? "active" : ""}`}
                    onClick={() => onSelectConversation(String(conv.id))}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        onSelectConversation(String(conv.id));
                      }
                    }}
                  >
                    <MessageSquare size={16} className="chat-item-icon" />
                    <span className="chat-item-title" title={conv.chat_title}>
                      {conv.chat_title}
                    </span>

                    {onDeleteConversation && (
                      <button
                        type="button"
                        className="chat-item-delete"
                        title="Delete chat"
                        onClick={(e) => {
                          e.stopPropagation();
                          onDeleteConversation(String(conv.id));
                        }}
                      >
                        <Trash2 size={13} />
                      </button>
                    )}
                  </div>
                );
              })
            ) : (
              <div className="no-chats-found">
                <span>{searchQuery ? "No matching chats" : "No recent chats"}</span>
              </div>
            )}
          </div>
        </div>

        {/* Bottom Section */}
        <div className="sidebar-bottom">
          <button type="button" className="sidebar-button">
            <Settings size={18} />
            <span>Settings</span>
          </button>

          <div className="user-profile">
            <div className="user-avatar">
              <User size={18} />
            </div>

            <div className="user-info">
              <strong>Player</strong>
              <span>Survivor • Lv. 32</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;