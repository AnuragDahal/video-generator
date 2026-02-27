import { useState, useCallback } from "react";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
}

const MOCK_RESPONSES = [
  "That's a great question! Let me think about this...\n\nBased on my analysis, here are a few key points:\n\n1. **First consideration** — The approach you're describing is quite common in modern web development.\n2. **Second point** — There are several ways to implement this, each with trade-offs.\n3. **Third insight** — I'd recommend starting with the simplest solution and iterating.\n\nWould you like me to elaborate on any of these points?",
  "Here's a code example that might help:\n\n```typescript\nconst greeting = (name: string): string => {\n  return `Hello, ${name}! Welcome to the AI chat.`;\n};\n\nconsole.log(greeting('World'));\n```\n\nThis demonstrates a simple TypeScript function with proper typing. Let me know if you'd like me to explain further!",
  "I'd be happy to help with that! Here's what I suggest:\n\n- Start by defining your **data model** clearly\n- Then build out the **UI components** one at a time\n- Finally, connect everything with **state management**\n\n> The best architecture is one that's easy to change.\n\nShall I walk you through any of these steps in detail?",
  "Interesting! Let me break this down:\n\n## Overview\nThe concept you're referring to involves several interconnected parts.\n\n## Key Components\n- **Component A**: Handles the core logic\n- **Component B**: Manages the UI layer\n- **Component C**: Orchestrates data flow\n\n## Recommendation\nI'd suggest focusing on Component A first, as it forms the foundation for everything else.\n\nWant me to dive deeper into any specific component?",
];

export function useChatStore() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<
    string | null
  >(null);

  const activeConversation =
    conversations.find((c) => c.id === activeConversationId) ?? null;

  const createConversation = useCallback(() => {
    const id = crypto.randomUUID();
    const conv: Conversation = {
      id,
      title: "New chat",
      messages: [],
      createdAt: new Date(),
    };
    setConversations((prev) => [conv, ...prev]);
    setActiveConversationId(id);
    return id;
  }, []);

  const deleteConversation = useCallback(
    (id: string) => {
      setConversations((prev) => prev.filter((c) => c.id !== id));
      if (activeConversationId === id) {
        setActiveConversationId(null);
      }
    },
    [activeConversationId],
  );

  const sendMessage = useCallback(
    async (content: string) => {
      let convId = activeConversationId;
      if (!convId) {
        convId = crypto.randomUUID();
        const conv: Conversation = {
          id: convId,
          title: content.slice(0, 40) + (content.length > 40 ? "..." : ""),
          messages: [],
          createdAt: new Date(),
        };
        setConversations((prev) => [conv, ...prev]);
        setActiveConversationId(convId);
      }

      const userMsg: Message = {
        id: crypto.randomUUID(),
        role: "user",
        content,
        timestamp: new Date(),
      };

      setConversations((prev) =>
        prev.map((c) => {
          if (c.id !== convId) return c;
          const updated = { ...c, messages: [...c.messages, userMsg] };
          if (c.messages.length === 0) {
            updated.title =
              content.slice(0, 40) + (content.length > 40 ? "..." : "");
          }
          return updated;
        }),
      );

      // Simulate streaming response
      const responseText =
        MOCK_RESPONSES[Math.floor(Math.random() * MOCK_RESPONSES.length)];
      const assistantId = crypto.randomUUID();

      // Start with empty assistant message
      const assistantMsg: Message = {
        id: assistantId,
        role: "assistant",
        content: "",
        timestamp: new Date(),
      };

      setConversations((prev) =>
        prev.map((c) =>
          c.id === convId
            ? { ...c, messages: [...c.messages, assistantMsg] }
            : c,
        ),
      );

      // Stream characters
      for (let i = 0; i <= responseText.length; i++) {
        await new Promise((r) => setTimeout(r, 8 + Math.random() * 12));
        const partial = responseText.slice(0, i);
        setConversations((prev) =>
          prev.map((c) =>
            c.id === convId
              ? {
                  ...c,
                  messages: c.messages.map((m) =>
                    m.id === assistantId ? { ...m, content: partial } : m,
                  ),
                }
              : c,
          ),
        );
      }
    },
    [activeConversationId],
  );

  return {
    conversations,
    activeConversation,
    activeConversationId,
    setActiveConversationId,
    createConversation,
    deleteConversation,
    sendMessage,
  };
}
