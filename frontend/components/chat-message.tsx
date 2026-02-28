import { memo } from "react";
import ReactMarkdown from "react-markdown";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Progress } from "@/components/ui/progress";
import { Sparkles, User, Play, Loader2, AlertCircle, FileVideo } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Message } from "@/lib/chat-store";

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage = memo(function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === "assistant";
  const isProcessing = message.status === "processing" || message.status === "pending";
  const isCompleted = message.status === "completed";
  const isFailed = message.status === "failed";

  return (
    <div className={cn("flex gap-4 px-4 py-8 max-w-4xl mx-auto", isAssistant && "bg-transparent")}>
      <Avatar className={cn("h-8 w-8 shrink-0 mt-0.5", isAssistant ? "bg-primary/15" : "bg-secondary")}>
        <AvatarFallback className={cn(isAssistant ? "bg-primary/15 text-primary" : "bg-secondary text-secondary-foreground")}>
          {isAssistant ? <Sparkles className="h-4 w-4" /> : <User className="h-4 w-4" />}
        </AvatarFallback>
      </Avatar>

      <div className="flex-1 min-w-0 space-y-4">
        <div className="flex items-center justify-between">
            <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                {isAssistant ? "NovaMind AI" : "You"}
            </p>
            {isAssistant && isProcessing && (
                <div className="flex items-center gap-2 text-[10px] font-medium text-primary animate-pulse">
                    <Loader2 className="h-3 w-3 animate-spin" />
                    GENERATING
                </div>
            )}
        </div>

        <div className="prose prose-invert prose-sm max-w-none text-foreground leading-relaxed">
          <ReactMarkdown>{message.content || ""}</ReactMarkdown>
        </div>

        {isAssistant && (
            <div className="mt-4 space-y-4">
                {/* Progress Bar for Active Tasks */}
                {isProcessing && (
                    <div className="space-y-2 max-w-sm">
                        <div className="flex justify-between text-[11px] font-medium text-muted-foreground">
                            <span>Pipeline Progress</span>
                            <span>{message.progress || 0}%</span>
                        </div>
                        <Progress value={message.progress || 0} className="h-1.5 bg-secondary" />
                    </div>
                )}

                {/* Video Preview Table/Card for Completed Tasks */}
                {isCompleted && message.videoUrl && (
                    <div className="group relative overflow-hidden rounded-xl border border-border bg-secondary/30 transition-all hover:border-primary/50 hover:bg-secondary/50 max-w-lg">
                        <div className="aspect-video w-full bg-slate-900 flex items-center justify-center relative">
                            {message.thumbnailUrl ? (
                                <img 
                                    src={message.thumbnailUrl} 
                                    alt="Video thumbnail" 
                                    className="w-full h-full object-cover transition-transform group-hover:scale-105"
                                />
                            ) : (
                                <FileVideo className="h-12 w-12 text-muted-foreground/30" />
                            )}
                            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                <a 
                                    href={message.videoUrl} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="bg-primary text-primary-foreground px-4 py-2 rounded-full flex items-center gap-2 text-sm font-semibold shadow-xl transform scale-90 group-hover:scale-100 transition-transform"
                                >
                                    <Play className="h-4 w-4 fill-current" />
                                    Watch Video
                                </a>
                            </div>
                        </div>
                        <div className="p-4 flex items-center justify-between">
                            <div className="space-y-1">
                                <h4 className="text-sm font-medium leading-none">Generation Complete</h4>
                                <p className="text-xs text-muted-foreground">High-quality MP4 ready for download</p>
                            </div>
                            <a 
                                href={message.videoUrl} 
                                download 
                                className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center hover:bg-primary hover:text-primary-foreground transition-colors"
                            >
                                <Play className="h-4 w-4" />
                            </a>
                        </div>
                    </div>
                )}

                {/* Error State */}
                {isFailed && (
                     <div className="flex items-start gap-2 p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive text-xs">
                        <AlertCircle className="h-4 w-4 shrink-0" />
                        <p>{message.content || "An error occurred during video generation."}</p>
                    </div>
                )}
            </div>
        )}
      </div>
    </div>
  );
});
