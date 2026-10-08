import React from "react";
import { Bot, Sparkles } from "lucide-react";

export const TypingIndicator: React.FC = () => {
  return (
    <div className="typing-indicator-container">
      <div className="message-avatar assistant-avatar pulse-glow">
        <Bot size={18} />
      </div>

      <div className="typing-bubble">
        <div className="typing-header">
          <span className="typing-label">Farewell Oregon AI is thinking</span>
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
