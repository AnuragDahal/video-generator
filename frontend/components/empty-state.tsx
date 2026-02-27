import { Sparkles } from "lucide-react";
import { motion } from "framer-motion";

const suggestions = [
  "Explain quantum computing in simple terms",
  "Help me write a React custom hook",
  "What are the best practices for TypeScript?",
  "Create a Python script to analyze data",
];

interface EmptyStateProps {
  onSuggestionClick: (text: string) => void;
}

export function EmptyState({ onSuggestionClick }: EmptyStateProps) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="flex flex-col items-center gap-6"
      >
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 border border-primary/20">
          <Sparkles className="h-8 w-8 text-primary" />
        </div>
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-foreground tracking-tight">
            How can I help you today?
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Ask me anything — I'm here to assist.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 mt-4 w-full max-w-lg">
          {suggestions.map((s, i) => (
            <motion.button
              key={s}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 + i * 0.08 }}
              onClick={() => onSuggestionClick(s)}
              className="rounded-xl border border-border bg-card px-4 py-3 text-left text-sm text-muted-foreground hover:text-foreground hover:border-primary/30 hover:bg-accent transition-all"
            >
              {s}
            </motion.button>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
