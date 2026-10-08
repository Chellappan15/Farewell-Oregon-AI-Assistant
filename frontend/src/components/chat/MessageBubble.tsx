import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { User, Bot, Copy, Check } from "lucide-react";
import type { ChatMessage } from "../../types/chat";

export interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === "user";

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy message:", err);
    }
  };

  return (
    <div className={`message-row ${isUser ? "user-row" : "assistant-row"}`}>
      <div className={`message-avatar ${isUser ? "user-avatar-bubble" : "assistant-avatar"}`}>
        {isUser ? <User size={17} /> : <Bot size={18} />}
      </div>

      <div className={`message-bubble ${isUser ? "user-bubble" : "assistant-bubble"}`}>
        <div className="message-header-meta">
          <span className="message-sender-name">
            {isUser ? "Survivor (Player)" : "Farewell Oregon AI Assistant"}
          </span>
          {message.timestamp && (
            <span className="message-timestamp">{message.timestamp}</span>
          )}

          <button
            type="button"
            className="message-copy-btn"
            onClick={handleCopy}
            title={copied ? "Copied!" : "Copy message"}
            aria-label="Copy message"
          >
            {copied ? <Check size={13} className="text-emerald" /> : <Copy size={13} />}
          </button>
        </div>

        <div className="message-content">
          {isUser ? (
            <p className="user-message-text">{message.content}</p>
          ) : (
            <div className="markdown-body">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
