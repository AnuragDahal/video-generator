import { memo } from "react";
import ReactMarkdown from "react-markdown";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Sparkles, User } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Message } from "@/lib/chat-store";

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage = memo(function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === "assistant";

  return (
    <div className={cn("flex gap-4 px-4 py-6 max-w-3xl mx-auto", isAssistant && "bg-transparent")}>
      <Avatar className={cn("h-8 w-8 shrink-0 mt-0.5", isAssistant ? "bg-primary/15" : "bg-secondary")}>
        <AvatarFallback className={cn(isAssistant ? "bg-primary/15 text-primary" : "bg-secondary text-secondary-foreground")}>
          {isAssistant ? <Sparkles className="h-4 w-4" /> : <User className="h-4 w-4" />}
        </AvatarFallback>
      </Avatar>

      <div className="flex-1 min-w-0 space-y-2">
        <p className="text-xs font-medium text-muted-foreground">{isAssistant ? "NovaMind" : "You"}</p>
        <div className="prose prose-invert prose-sm max-w-none text-foreground [&_pre]:bg-secondary [&_pre]:rounded-lg [&_pre]:p-4 [&_code]:text-primary [&_code]:bg-secondary [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-xs [&_pre_code]:bg-transparent [&_pre_code]:p-0 [&_strong]:text-foreground [&_blockquote]:border-primary/30 [&_blockquote]:text-muted-foreground [&_h2]:text-foreground [&_h2]:text-base [&_li]:marker:text-muted-foreground">
          <ReactMarkdown>{message.content || "▊"}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
});
