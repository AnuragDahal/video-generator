"use client";
import { useRef, useEffect, useState } from "react";
import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ChatSidebar } from "@/components/chat-sidebar";
import { ChatMessage } from "@/components/chat-message";
import { ChatInput } from "@/components/chat-input";
import { EmptyState } from "@/components/empty-state";
import { useChatStore } from "@/lib/chat-store";
import { cn } from "@/lib/utils";
import { useIsMobile } from "@/hooks/use-mobile";

const page = () => {
  const {
    conversations,
    activeConversation,
    activeConversationId,
    setActiveConversationId,
    createConversation,
    deleteConversation,
    sendMessage,
  } = useChatStore();

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const isMobile = useIsMobile();

  // Auto-close sidebar on mobile
  useEffect(() => {
    if (isMobile) setSidebarOpen(false);
  }, [isMobile]);

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

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      {/* Sidebar */}
      <div
        className={cn(
          "shrink-0 transition-all duration-300 overflow-hidden",
          sidebarOpen ? "w-64" : "w-0",
          isMobile && sidebarOpen && "absolute inset-y-0 left-0 z-50 w-64",
        )}
      >
        <ChatSidebar
          conversations={conversations}
          activeId={activeConversationId}
          onSelect={(id) => {
            setActiveConversationId(id);
            if (isMobile) setSidebarOpen(false);
          }}
          onCreate={() => {
            createConversation();
            if (isMobile) setSidebarOpen(false);
          }}
          onDelete={deleteConversation}
        />
      </div>

      {/* Overlay for mobile sidebar */}
      {isMobile && sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Chat */}
      <div className="flex flex-1 flex-col min-w-0">
        {/* Top Bar */}
        <header className="flex items-center gap-3 border-b border-border px-4 h-13 shrink-0">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="h-8 w-8 text-muted-foreground hover:text-foreground"
          >
            <Menu className="h-4 w-4" />
          </Button>
          <span className="text-sm font-medium text-muted-foreground truncate">
            {activeConversation?.title ?? "New chat"}
          </span>
        </header>

        {/* Messages or Empty State */}
        {messages.length === 0 ? (
          <EmptyState onSuggestionClick={handleSend} />
        ) : (
          <ScrollArea className="flex-1">
            <div className="divide-y divide-border/30">
              {messages.map((msg) => (
                <ChatMessage key={msg.id} message={msg} />
              ))}
            </div>
            <div ref={bottomRef} />
          </ScrollArea>
        )}

        {/* Input */}
        <ChatInput onSend={handleSend} disabled={isSending} />
      </div>
    </div>
  );
};

export default page;
