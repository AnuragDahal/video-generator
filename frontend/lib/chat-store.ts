import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import api from "./api";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  status?: "pending" | "processing" | "completed" | "failed";
  progress?: number;
  taskId?: string;
  videoUrl?: string;
  thumbnailUrl?: string;
  timestamp: string; // Store as string for JSON serialization
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: string;
}

interface ChatState {
  conversations: Conversation[];
  activeConversationId: string | null;
  activeConversation: Conversation | null;
  
  // Actions
  setActiveConversationId: (id: string | null) => void;
  createConversation: () => string;
  deleteConversation: (id: string) => void;
  sendMessage: (content: string) => Promise<void>;
  updateMessage: (convId: string, messageId: string, updates: Partial<Message>) => void;
  reconnectSSE: (convId: string, messageId: string, taskId: string) => void;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      conversations: [],
      activeConversationId: null,

      activeConversation: null,

      setActiveConversationId: (id) => set((state) => ({ 
        activeConversationId: id,
        activeConversation: state.conversations.find((c) => c.id === id) || null
      })),

      createConversation: () => {
        const id = crypto.randomUUID();
        const newConv: Conversation = {
          id,
          title: "New video project",
          messages: [],
          createdAt: new Date().toISOString(),
        };
        set((state) => ({
          conversations: [newConv, ...state.conversations],
          activeConversationId: id,
          activeConversation: newConv
        }));
        return id;
      },

      deleteConversation: (id) => {
        set((state) => {
          const newConvs = state.conversations.filter((c) => c.id !== id);
          const nextActiveId = state.activeConversationId === id ? null : state.activeConversationId;
          return {
            conversations: newConvs,
            activeConversationId: nextActiveId,
            activeConversation: newConvs.find(c => c.id === nextActiveId) || null
          };
        });
      },

      updateMessage: (convId, messageId, updates) => {
        set((state) => {
          const newConversations = state.conversations.map((c) => {
            if (c.id !== convId) return c;
            return {
              ...c,
              messages: c.messages.map((m) => (m.id === messageId ? { ...m, ...updates } : m)),
            };
          });
          return {
            conversations: newConversations,
            activeConversation: newConversations.find(c => c.id === state.activeConversationId) || null
          };
        });
      },

      sendMessage: async (content) => {
        const state = get();
        let convId = state.activeConversationId;
        
        if (!convId) {
          convId = state.createConversation();
        }

        const userMsg: Message = {
          id: crypto.randomUUID(),
          role: "user",
          content,
          timestamp: new Date().toISOString(),
        };

        // Add user message
        set((state) => ({
          conversations: state.conversations.map((c) => {
            if (c.id !== convId) return c;
            const updated = { ...c, messages: [...c.messages, userMsg] };
            if (c.messages.length === 0 || c.title === "New video project") {
              updated.title = content.slice(0, 40) + (content.length > 40 ? "..." : "");
            }
            return updated;
          }),
        }));

        const assistantId = crypto.randomUUID();
        const assistantMsg: Message = {
          id: assistantId,
          role: "assistant",
          content: "Initializing generation...",
          status: "pending",
          progress: 0,
          timestamp: new Date().toISOString(),
        };

        // Add assistant placeholder
        set((state) => ({
          conversations: state.conversations.map((c) =>
            c.id === convId ? { ...c, messages: [...c.messages, assistantMsg] } : c
          ),
        }));

        try {
          const response = await api.post("/video/generate", { prompt: content });
          const { task_id } = response.data;
          
          // Start SSE tracking
          get().updateMessage(convId!, assistantId, { taskId: task_id });
          get().reconnectSSE(convId!, assistantId, task_id);

        } catch (error: any) {
          get().updateMessage(convId!, assistantId, {
            content: `Error: ${error.response?.data?.detail || error.message || "Failed to connect to backend"}`,
            status: "failed",
          });
        }
      },

      reconnectSSE: (convId, messageId, taskId) => {
        const baseURL = process.env.NEXT_PUBLIC_API_URL?.replace("/api/v1", "") || "http://localhost:8000";
        const eventSource = new EventSource(`${baseURL}/api/v1/video/stream/${taskId}`);

        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            get().updateMessage(convId, messageId, {
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
          eventSource.close();
        };
      },
    }),
    {
      name: "video-generator-storage",
      storage: createJSONStorage(() => localStorage),
    }
  )
);
