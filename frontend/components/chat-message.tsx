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
    <div 
      className={cn(
        "flex w-full gap-3 px-4 py-6",
        isAssistant ? "justify-start" : "justify-end"
      )}
    >
      <div 
        className={cn(
            "flex max-w-[80%] sm:max-w-[70%] gap-3",
            isAssistant ? "flex-row" : "flex-row-reverse"
        )}
      >
        <Avatar className={cn("h-8 w-8 shrink-0 mt-0.5 shadow-sm cursor-pointer hover:opacity-80 transition-opacity", isAssistant ? "bg-primary/10" : "bg-primary")}>
            <AvatarFallback className={cn(isAssistant ? "bg-primary/10 text-primary" : "bg-primary text-primary-foreground")}>
            {isAssistant ? <Sparkles className="h-4 w-4" /> : <User className="h-4 w-4" />}
            </AvatarFallback>
        </Avatar>

        <div className={cn("flex flex-col space-y-2", isAssistant ? "items-start" : "items-end")}>
            <div className="flex items-center gap-2">
                <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground/70">
                    {isAssistant ? "NovaMind AI" : "You"}
                </p>
                {isAssistant && isProcessing && (
                    <div className="flex items-center gap-1 text-[9px] font-bold text-primary animate-pulse">
                        <Loader2 className="h-2.5 w-2.5 animate-spin" />
                        GENERATING
                    </div>
                )}
            </div>

            <div 
                className={cn(
                    "rounded-2xl px-4 py-3 shadow-sm border leading-relaxed text-sm",
                    isAssistant 
                        ? "bg-secondary/30 border-border/50 rounded-tl-none text-foreground" 
                        : "bg-primary/5 border-primary/20 rounded-tr-none text-foreground"
                )}
            >
                <div className="prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-pre:bg-zinc-950 prose-pre:border prose-pre:border-white/10">
                    <ReactMarkdown>{message.content || ""}</ReactMarkdown>
                </div>

                {isAssistant && (
                    <div className="mt-4 space-y-4">
                        {/* Progress Bar for Active Tasks */}
                        {isProcessing && (
                            <div className="space-y-2 w-full min-w-[200px]">
                                <div className="flex justify-between text-[10px] font-semibold text-muted-foreground">
                                    <span>Pipeline Progress</span>
                                    <span>{message.progress || 0}%</span>
                                </div>
                                <Progress value={message.progress || 0} className="h-1 bg-secondary" />
                            </div>
                        )}

                        {/* Video Preview Table/Card for Completed Tasks */}
                        {isCompleted && message.videoUrl && (
                            <div className="group relative overflow-hidden rounded-xl border border-border bg-background/50 transition-all hover:border-primary/50 hover:bg-background/80 w-full min-w-[240px] max-w-sm">
                                <div className="aspect-video w-full bg-slate-950 flex items-center justify-center relative">
                                    {message.thumbnailUrl ? (
                                        <img 
                                            src={message.thumbnailUrl} 
                                            alt="Video thumbnail" 
                                            className="w-full h-full object-cover transition-transform group-hover:scale-105"
                                        />
                                    ) : (
                                        <FileVideo className="h-10 w-10 text-muted-foreground/20" />
                                    )}
                                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                        <a 
                                            href={message.videoUrl} 
                                            target="_blank" 
                                            rel="noopener noreferrer"
                                            className="bg-primary text-primary-foreground px-4 py-2 rounded-full flex items-center gap-2 text-xs font-semibold shadow-xl transform scale-90 group-hover:scale-100 transition-transform"
                                        >
                                            <Play className="h-3 w-3 fill-current" />
                                            Watch Video
                                        </a>
                                    </div>
                                </div>
                                <div className="p-3 flex items-center justify-between">
                                    <div className="space-y-0.5">
                                        <h4 className="text-[11px] font-bold leading-none">Generation Complete</h4>
                                        <p className="text-[10px] text-muted-foreground">MP4 ready</p>
                                    </div>
                                    <a 
                                        href={message.videoUrl} 
                                        download 
                                        className="h-7 w-7 rounded-full bg-secondary flex items-center justify-center hover:bg-primary hover:text-primary-foreground transition-colors"
                                    >
                                        <Play className="h-3 w-3" />
                                    </a>
                                </div>
                            </div>
                        )}

                        {/* Error State */}
                        {isFailed && (
                            <div className="flex items-start gap-2 p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive text-[11px] font-medium">
                                <AlertCircle className="h-3.5 w-3.5 shrink-0" />
                                <p>{message.content || "An error occurred during video generation."}</p>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
      </div>
    </div>
  );
});
