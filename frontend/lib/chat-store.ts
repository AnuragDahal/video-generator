import { useState, useCallback } from "react";
import api from "./api";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  status?: "pending" | "processing" | "completed" | "failed";
  progress?: number;
  videoUrl?: string;
  thumbnailUrl?: string;
  timestamp: Date;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
}

export function useChatStore() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);

  const activeConversation = conversations.find((c) => c.id === activeConversationId) ?? null;

  const createConversation = useCallback(() => {
    const id = crypto.randomUUID();
    const conv: Conversation = {
      id,
      title: "New video project",
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
    [activeConversationId]
  );

  const updateMessage = useCallback((convId: string, messageId: string, updates: Partial<Message>) => {
    setConversations((prev) =>
      prev.map((c) => {
        if (c.id !== convId) return c;
        return {
          ...c,
          messages: c.messages.map((m) => (m.id === messageId ? { ...m, ...updates } : m)),
        };
      })
    );
  }, []);

  const sendMessage = useCallback(
    async (content: string) => {
      let convId = activeConversationId;
      if (!convId) {
        convId = createConversation();
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
            updated.title = content.slice(0, 40) + (content.length > 40 ? "..." : "");
          }
          return updated;
        })
      );

      const assistantId = crypto.randomUUID();
      const assistantMsg: Message = {
        id: assistantId,
        role: "assistant",
        content: "Initializing generation...",
        status: "pending",
        progress: 0,
        timestamp: new Date(),
      };

      setConversations((prev) =>
        prev.map((c) =>
          c.id === convId ? { ...c, messages: [...c.messages, assistantMsg] } : c
        )
      );

      try {
        // 1. Request video generation
        const response = await api.post("/video/generate", { prompt: content });
        const { task_id } = response.data;

        // 2. Connect to SSE for progress updates
        const baseURL = process.env.NEXT_PUBLIC_API_URL?.replace("/api/v1", "") || "http://localhost:8000";
        const eventSource = new EventSource(`${baseURL}/api/v1/video/stream/${task_id}`);

        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            
            updateMessage(convId!, assistantId, {
              content: data.message || "Generating...",
              status: data.status,
              progress: data.progress,
              videoUrl: data.data?.video_url,
              thumbnailUrl: data.data?.thumbnail_url,
            });

            if (data.status === "completed" || data.status === "failed") {
              eventSource.close();
            }
          } catch (err) {
            console.error("Error parsing SSE data:", err);
          }
        };

        eventSource.onerror = (err) => {
          console.error("SSE Connection Error:", err);
          updateMessage(convId!, assistantId, {
            content: "Connection to server lost. Checking status...",
            status: "failed",
          });
          eventSource.close();
        };

      } catch (error: any) {
        console.error("Failed to start generation:", error);
        updateMessage(convId!, assistantId, {
          content: `Error: ${error.response?.data?.detail || error.message || "Failed to connect to backend"}`,
          status: "failed",
        });
      }
    },
    [activeConversationId, createConversation, updateMessage]
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
