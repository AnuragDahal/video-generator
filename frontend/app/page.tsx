"use client";
import { ChatInput } from "@/components/chat-input";
import { ChatMessage } from "@/components/chat-message";
import { ChatSidebar } from "@/components/chat-sidebar";
import { EmptyState } from "@/components/empty-state";
import { ScrollArea } from "@/components/ui/scroll-area";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { useChatStore } from "@/lib/chat-store";
import { useEffect, useRef, useState } from "react";

const page = () => {
  const {
    conversations,
    activeConversation,
    activeConversationId,
    setActiveConversationId,
    createConversation,
    deleteConversation,
    sendMessage,
    reconnectSSE,
  } = useChatStore();

  const [isSending, setIsSending] = useState(false);
  const [mounted, setMounted] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Handle hydration and reconnection
  useEffect(() => {
    setMounted(true);
    
    // Check all conversations for active tasks and reconnect SSE
    conversations.forEach((conv) => {
      conv.messages.forEach((msg) => {
        if ((msg.status === "processing" || msg.status === "pending") && msg.taskId) {
           reconnectSSE(conv.id, msg.id, msg.taskId);
        }
      });
    });
  }, []);

  // Scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeConversation?.messages]);

  const handleSend = async (content: string) => {
    setIsSending(true);
    await sendMessage(content);
    setIsSending(false);
  };

  const messages = activeConversation?.messages ?? [];

  if (!mounted) return null;

  return (
    <SidebarProvider>
      <ChatSidebar
        conversations={conversations}
        activeId={activeConversationId}
        onConversationSelect={(id) => {
          setActiveConversationId(id);
        }}
        onCreate={() => {
          createConversation();
        }}
        onDelete={deleteConversation}
      />

      <SidebarInset>
        {/* Top Bar */}
        <header className="flex h-14 shrink-0 items-center gap-2 border-b px-4">
           <SidebarTrigger className="-ml-1" />
           <div className="flex-1">
              <span className="text-sm font-medium text-muted-foreground truncate">
                {activeConversation?.title ?? "New chat"}
              </span>
           </div>
        </header>

        <div className="flex flex-1 flex-col overflow-hidden">
          {/* Messages or Empty State */}
          {messages.length === 0 ? (
            <EmptyState onSuggestionClick={handleSend} />
          ) : (
            <ScrollArea className="flex-1">
              <div className="flex flex-col">
                {messages.map((msg: any) => (
                  <ChatMessage key={msg.id} message={msg} />
                ))}
              </div>
              <div ref={bottomRef} />
            </ScrollArea>
          )}

          {/* Input */}
          <ChatInput onSend={handleSend} disabled={isSending} />
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
};

export default page;
