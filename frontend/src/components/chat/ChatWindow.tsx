import React from "react"; 
import MessageList from "./MessageList"; 
import ChatInput from "./ChatInput"; 
import type { ChatMessage } from "../../types/chat"; 

export interface ChatWindowProps { 
  messages: ChatMessage[]; 
  isLoading: boolean; 
  isMessagesLoading?: boolean;
  onSendMessage: (content: string) => void; 
  onSelectPrompt?: (prompt: string) => void; 
} 

export const ChatWindow: React.FC<ChatWindowProps> = ({ 
  messages, 
  isLoading, 
  isMessagesLoading = false,
  onSendMessage, 
  onSelectPrompt, 
}) => { 
  return ( 
    <section className="chat-window-section"> 
      <div className="chat-window-messages"> 
        <MessageList 
          messages={messages} 
          isLoading={isLoading} 
          isMessagesLoading={isMessagesLoading}
          onSelectPrompt={onSelectPrompt} 
        /> 
      </div> 
      <div className="chat-window-input-area"> 
        <ChatInput onSendMessage={onSendMessage} disabled={isLoading || isMessagesLoading} /> 
      </div> 
    </section> 
  ); 
}; 
    
export default ChatWindow;