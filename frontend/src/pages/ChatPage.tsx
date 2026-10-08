import React, { useContext, useState } from "react";
import MainLayout from "../components/layout/MainLayout";
import type { Conversation, ChatMessage } from "../types/chat";
import ChatContext from "../context/ChatContext";

const INITIAL_CONVERSATIONS: Conversation[] = [
  {
    id: "conv-1",
    title: "Breaker strategy",
    lastUpdated: "Just now",
    messages: [
      {
        role: "user",
        content: "What is the best tactical strategy to take down a Breaker without wasting all my ammo?",
        timestamp: "10:24 AM",
      },
      {
        role: "assistant",
        content: `### ☠ Tactical Briefing: Breaker Elimination

Breakers are massive, mutated Freakers with immense health pools and heavy melee resistance. Engaging in direct head-to-head combat or melee will deplete your resources rapidly.

#### 🎯 Key Weaknesses & Mechanics
* **Fire Vulnerability**: Breakers take substantial damage over time from fire, which also slows their charge velocity.
* **Stealth Takedown**: Requires the **Executioner** skill in the Melee skill tree. Without this skill, stealth attacks will fail.
* **Stagger Windows**: High-caliber sniper rounds (e.g., .50 BFG) or Headshots with the Chicago Chopper create momentary stagger windows.

---

#### 🛠 Recommended Loadout
1. **Primary**: Chicago Chopper or US556 (Rapid sustained fire)
2. **Special**: **.50 BFG** (2-3 precision headshots will eliminate a Breaker) or **Crossbow** with Residue Bolts
3. **Consumables**: Molotov Cocktails, Napalm Molotovs, Smoke Bombs

> **Tactical Field Tip:**
> If other Freakers or Swarmers are nearby, fire a **Residue Bolt** into the Breaker. Its hyper-aggressive AI will trigger it to attack and eliminate the entire nearby swarm for you before taking lethal damage!`,
        timestamp: "10:25 AM",
      },
    ],
  },
  {
    id: "conv-2",
    title: "RPD machine gun",
    lastUpdated: "2 hours ago",
    messages: [
      {
        role: "user",
        content: "Where do I unlock the RPD machine gun and is it worth the credits?",
        timestamp: "08:15 AM",
      },
      {
        role: "assistant",
        content: `### ⚔ Armory Intel: RPD Light Machine Gun

The **RPD** is one of the premier special weapons in Days Gone for Horde extermination.

* **Merchant Location**: Wizard Island Merchant (Crater Lake region)
* **Trust Requirement**: Trust Level 3 with Wizard Island
* **Capacity**: High base drum magazine (expanded further with camp magazine upgrades)

#### Verdict
**Essential Investment.** When paired with Focus cocktails, the RPD provides unmatched crowd-clearing DPS against Southern hordes.`,
        timestamp: "08:16 AM",
      },
    ],
  },
  {
    id: "conv-3",
    title: "Best weapon for hordes",
    lastUpdated: "Yesterday",
    messages: [
      {
        role: "user",
        content: "What is the absolute best weapon loadout for clearing late-game hordes?",
        timestamp: "Yesterday",
      },
      {
        role: "assistant",
        content: `### 🛡 Endgame Horde Hunting Loadout

For mega-hordes (such as Sawmill Horde or Iron Butte):

1. **Primary**: **Chicago Chopper** (Wizard Island Trust 3) — highest clip size and damage density.
2. **Sidearm**: **SMP9 (Mil-Spec)** — Unlocked by completing 4 Horde Killer milestones.
3. **Special**: **MG 55** (Reward for 60% Horde Killer completion) or **BFG .50**.
4. **Explosives**: Attractor Bombs + Napalm Molotovs for bottleneck choke points.`,
        timestamp: "Yesterday",
      },
    ],
  },
  {
    id: "conv-4",
    title: "How to kill Screamers",
    lastUpdated: "3 days ago",
    messages: [
      {
        role: "user",
        content: "How do I deal with Screamers before they stun me?",
        timestamp: "3 days ago",
      },
      {
        role: "assistant",
        content: `### 🔊 Screamer Countermeasures

* **Acoustic Disruption**: Her sonic scream instantly drains Deacon's stamina, blurs vision, and summons all nearby Freakers.
* **Strategy**: Always engage from distance using a suppressed sniper rifle or crossbow headshot before she detects your presence. If spotted, immediately dodge-roll or break line of sight.`,
        timestamp: "3 days ago",
      },
    ],
  },
];

export const ChatPage: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>(INITIAL_CONVERSATIONS);
  const [activeId, setActiveId] = useState<string>("conv-1");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isMessagesLoading, setIsMessagesLoading] = useState<boolean>(false);
  
  const chatContext = useContext(ChatContext);

  const activeConversation = conversations.find((c) => c.id === activeId);
  const activeMessages = activeConversation ? activeConversation.messages : [];

  const handleSelectConversation = (id: string) => {
    setActiveId(id);
    setIsMessagesLoading(true);
    // Simulate tactical message loading transition
    setTimeout(() => {
      setIsMessagesLoading(false);
    }, 300);
  };

  const handleNewChat = () => {
    const newId = `conv-${Date.now()}`;
    const newConv: Conversation = {
      id: newId,
      title: "New Survival Briefing",
      lastUpdated: "Just now",
      messages: [],
    };

    setConversations((prev) => [newConv, ...prev]);
    setActiveId(newId);
    setIsMessagesLoading(false);
  };

  const handleDeleteConversation = (id: string) => {
    setConversations((prev) => {
      const filtered = prev.filter((c) => c.id !== id);
      if (activeId === id) {
        if (filtered.length > 0) {
          setActiveId(filtered[0].id);
        } else {
          // If all deleted, generate new blank chat
          const blankId = `conv-${Date.now()}`;
          setActiveId(blankId);
          return [
            {
              id: blankId,
              title: "New Survival Briefing",
              lastUpdated: "Just now",
              messages: [],
            },
          ];
        }
      }
      return filtered;
    });
  };

  const handleClearChat = () => {
    setConversations((prev) =>
      prev.map((c) => (c.id === activeId ? { ...c, messages: [] } : c))
    );
  };

  const handleSendMessage = (text: string) => {
    const userMessage: ChatMessage = {
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    // Update conversation title if it was a new chat
    setConversations((prev) =>
      prev.map((c) => {
        if (c.id === activeId) {
          const isFirstMessage = c.messages.length === 0;
          return {
            ...c,
            title: isFirstMessage
              ? text.length > 28
                ? text.slice(0, 28) + "..."
                : text
              : c.title,
            lastUpdated: "Just now",
            messages: [...c.messages, userMessage],
          };
        }
        return c;
      })
    );

    setIsLoading(true);

    // Simulate realistic AI generation with Days Gone intelligence
    setTimeout(() => {
      const responseContent = generateTacticalResponse(text);

      const aiMessage: ChatMessage = {
        role: "assistant",
        content: responseContent,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setConversations((prev) =>
        prev.map((c) =>
          c.id === activeId
            ? { ...c, messages: [...c.messages, aiMessage] }
            : c
        )
      );

      setIsLoading(false);
    }, 1100);
  };

  return (
    <MainLayout
      conversations={conversations}
      activeConversationId={activeId}
      onSelectConversation={handleSelectConversation}
      onNewChat={handleNewChat}
      onDeleteConversation={handleDeleteConversation}
      messages={activeMessages}
      isLoading={isLoading}
      isMessagesLoading={isMessagesLoading}
      onSendMessage={handleSendMessage}
      onSelectPrompt={handleSendMessage}
      onClearChat={handleClearChat}
      chatHistory={chatContext?.chatList ?? []}
    />
  );
};

// Tactical response simulation for Days Gone UI
function generateTacticalResponse(query: string): string {
  const lower = query.toLowerCase();

  if (lower.includes("breaker")) {
    return `### ☠ Breaker Combat Protocol

* **Threat Level**: Very High (Armored Freaker)
* **Primary Tactic**: Keep distance using the bike or high vantage points.
* **Weapon Recommendation**: .50 BFG or Napalm Molotovs to strip armor.
* **Residue Bolting**: Shoot with a Residue Bolt to turn it against other nearby Freakers.`;
  }

  if (lower.includes("weapon") || lower.includes("saf") || lower.includes("mws") || lower.includes("compare")) {
    return `### ⚔ Tactical Weapon Analysis: SAF vs MWS

| Weapon | Damage | Fire Rate | Accuracy | Magazine | Best Suited For |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **SAF** | Moderate | Medium | 74% | 30 | Medium range, steady tap-firing |
| **MWS** | High | High | 82% | 35 | Sustained horde defense & run-and-gun |

**Field Verdict**: The **MWS** offers significantly tighter spread during sustained fire bursts and faster reload cycles, making it the superior primary rifle for navigating early Copeland & Tucker territory.`;
  }

  if (lower.includes("horde") || lower.includes("sawmill") || lower.includes("iron butte")) {
    return `### 🛡 Horde Extermination Strategy

When engaging hordes in the Pacific Northwest:

1. **Scout Choke Points**: Identify nearby tunnels, tight cliff passes, and red fuel barrels before alerting the swarm.
2. **Plant Traps**: Lay Proximity Mines and Remote Bombs along your planned retreat path.
3. **Attractor Clustering**: Throw an Attractor into a dense cluster, followed immediately by a **Napalm Molotov**.
4. **Stamina Management**: Always consume a Stamina Cocktail before the swarm initiates pursuit.`;
  }

  if (lower.includes("kerosene") || lower.includes("nest") || lower.includes("craft") || lower.includes("scavenge")) {
    return `### 🎒 Scavenging Intel: Essential Crafting Components

* **Kerosene**: Found most commonly in NERO Checkpoints, gas stations (near pumps and tow trucks), and mechanic garages.
* **Nest Residue**: Collect from burned-out Infestation Nests after clearing them with Molotovs.
* **Polystyrene**: Found in abandoned pickup truck beds and warehouse shipping crates. Used to fabricate Napalm Molotovs.`;
  }

  return `### 🌲 Farewell Oregon AI Field Report

Received query: **"${query}"**

#### Tactical Assessment:
* **Oregon Wasteland Context**: Freaker movement patterns fluctuate based on weather and day/night cycles. Horde concentration increases significantly at dusk near feeding grounds.
* **Survivor Directive**: Ensure Deacon's motorcycle is fueled and parked facing an open exit path before engaging hostiles in this zone.

> **Field Note**: Stay crouched in tall brush to conceal your thermal and acoustic signature from wandering Freaker scouts.`;
}

export default ChatPage;
