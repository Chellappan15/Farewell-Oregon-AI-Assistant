import React from "react";
import { Bot, Sparkles } from "lucide-react";
import { useChat } from "../../context/ChatContext";
import { getGameProfile } from "../../utils/games";

export const TypingIndicator: React.FC = () => {
  const profile = getGameProfile(useChat().game);

  return (
    <div className="typing-indicator-container">
      <div className="message-avatar assistant-avatar pulse-glow">
        <Bot size={18} />
      </div>

      <div className="typing-bubble">
        <div className="typing-header">
          <span className="typing-label">{profile.assistantName} is thinking</span>
          <Sparkles size={13} className="typing-sparkle" />
        </div>

        <div className="typing-dots">
          <span className="dot dot-1" />
          <span className="dot dot-2" />
          <span className="dot dot-3" />
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
