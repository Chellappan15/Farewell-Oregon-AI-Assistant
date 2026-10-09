import React, { useState } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";
import ChatWindow from "../chat/ChatWindow";
import IntelligencePanel from "../intelligence/IntelligencePanel";

export const MainLayout: React.FC = () => {
  const [sidebarMobileOpen, setSidebarMobileOpen] = useState(false);
  const [intelligenceOpen, setIntelligenceOpen] = useState(true);

  return (
    <div className="app-layout">
      {/* Sidebar - responsive desktop / mobile */}
      <Sidebar
        isOpen={sidebarMobileOpen}
        onClose={() => setSidebarMobileOpen(false)}
      />

      {/* Main Content Area */}
      <div className="main-content">
        <Header
          onToggleSidebar={() => setSidebarMobileOpen((prev) => !prev)}
          onToggleIntelligence={() => setIntelligenceOpen((prev) => !prev)}
          isIntelligenceOpen={intelligenceOpen}
        />

        <div className="content-area">
          <ChatWindow />

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