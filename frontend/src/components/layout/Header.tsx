import React from "react";
import {
  Menu,
  // RotateCcw,
  Cpu,
  Radio,
  Loader2,
} from "lucide-react";
import { useChat } from "../../context/ChatContext";
import IconButton from "../common/IconButton";
import Badge from "../common/Badge";

export interface HeaderProps {
  onToggleSidebar?: () => void;
  onToggleIntelligence?: () => void;
  isIntelligenceOpen?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onToggleSidebar,
  onToggleIntelligence,
  isIntelligenceOpen = true,
}) => {
  const { isMessagesLoading, serverStatus } = useChat();

  return (
    <header className="app-header">
      <div className="header-left">
        {onToggleSidebar && (
          <IconButton
            icon={<Menu size={20} />}
            label="Toggle Sidebar"
            onClick={onToggleSidebar}
            className="mobile-sidebar-toggle"
          />
        )}

        <div className="header-branding">
          <div className="header-title-wrapper">
            <h1 className="header-title">Days Gone Assistant</h1>
            <Badge variant={serverStatus ? "success" : "warning"} size="sm" dot dotClassName={serverStatus ? "badge-dot-success" : "badge-dot-failure"} className="header-status-badge">
              <p style={{color: serverStatus ? "#10b981" : "#ef4444"}}>{serverStatus ? "AI Online" : "AI Offline"}</p>
            </Badge>
          </div>
          <p className="header-subtitle">Survival intelligence for Days Gone</p>
        </div>
      </div>

      <div className="header-actions">
        {isMessagesLoading ? (
          <div className="header-loading-tag">
            <Loader2 size={14} className="header-loading-spinner" />
            <span className="indicator-text">Loading Intel...</span>
          </div>
        ) : (
          <div className="header-indicator">
            <Radio size={14} className={serverStatus ? "radio-pulse-success" : "radio-pulse-failure" } />
            <span className="indicator-text">Oregon Radio Link {serverStatus ? "Active" : "Inactive"}</span>
          </div>
        )}

        {/* {!isMessagesLoading && messages.length > 0 && (
          <IconButton
            icon={<RotateCcw size={16} />}
            label="Clear current conversation"
            variant="ghost"
            size="md"
            onClick={clearActiveChat}
          />
        )} */}

        {onToggleIntelligence && (
          <IconButton
            icon={<Cpu size={18} />}
            label="Toggle AI Intelligence Panel"
            variant={isIntelligenceOpen ? "primary" : "ghost"}
            size="md"
            active={isIntelligenceOpen}
            onClick={onToggleIntelligence}
          />
        )}
      </div>
    </header>
  );
};

export default Header;