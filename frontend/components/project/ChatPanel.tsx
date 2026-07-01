"use client";

import { useEffect, useRef, useState } from "react";
import { apiFetch } from "@/lib/api";
import type { ChatMessage, LocalChatMessage } from "@/types/chat";

type Props = {
  projectId: string;
};

const STARTER_PROMPTS = [
  "What does this project do?",
  "Where is authentication handled?",
  "Which files seem most important?",
  "What should I refactor first?",
];


export default function ChatPanel({ projectId }: Props) {
  const [messages, setMessages] = useState<LocalChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");

  const bottomRef = useRef<HTMLDivElement | null>(null);
  const shouldScrollRef = useRef(false);

  useEffect(() => {
    async function loadHistory() {
      try {
        const data: ChatMessage[] = await apiFetch(
          `/projects/${projectId}/chat`,
          { auth: true }
        );

        setMessages(
          data.map((item) => ({
            id: String(item.id),
            role: item.role,
            message: item.message,
          }))
        );
      } catch {
        setError("Could not load chat history.");
      } finally {
        setLoadingHistory(false);
      }
    }

    loadHistory();
  }, [projectId]);

  useEffect(() => {
    if (!shouldScrollRef.current) return;
  
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    shouldScrollRef.current = false;
  }, [messages]);

  async function sendMessage(messageText?: string) {
    const message = (messageText || input).trim();

    if (!message || sending) return;

    setError("");
    setInput("");

    const userMessage: LocalChatMessage = {
      id: `local-user-${Date.now()}`,
      role: "user",
      message,
    };
    
    shouldScrollRef.current = true;
    setMessages((prev) => [...prev, userMessage]);
    setSending(true);

    try {
      const data = await apiFetch(`/projects/${projectId}/chat`, {
        method: "POST",
        auth: true,
        body: JSON.stringify({ message }),
      });

      const assistantMessage: LocalChatMessage = {
        id: `local-assistant-${Date.now()}`,
        role: "assistant",
        message: data.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err.message || "Failed to send message.");
    } finally {
      setSending(false);
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    sendMessage();
  }

  return (
    <section className="rounded border p-4 space-y-4">
      <div>
        <h2 className="text-xl font-semibold">AI Repository Assistant</h2>
        <p className="text-sm text-gray-500">
          Ask questions about the latest scanned repository.
        </p>
      </div>

      {messages.length === 0 && !loadingHistory && (
        <div className="space-y-2">
          <p className="text-sm font-medium">Try asking:</p>

          <div className="flex flex-wrap gap-2">
            {STARTER_PROMPTS.map((prompt) => (
              <button
                key={prompt}
                onClick={() => sendMessage(prompt)}
                className="rounded border px-3 py-1 text-sm hover:bg-gray-50"
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="h-[420px] overflow-y-auto rounded bg-gray-50 p-3 space-y-3">
        {loadingHistory ? (
          <p className="text-sm text-gray-500">Loading chat history...</p>
        ) : messages.length === 0 ? (
          <p className="text-sm text-gray-500">
            No messages yet. Ask your first repository question.
          </p>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`rounded p-3 text-sm ${
                message.role === "user"
                  ? "ml-auto max-w-[85%] bg-black text-white"
                  : "mr-auto max-w-[90%] bg-white border"
              }`}
            >
              <p className="mb-1 text-xs opacity-70">
                {message.role === "user" ? "You" : "DevLens"}
              </p>
              <p className="whitespace-pre-line">{message.message}</p>
            </div>
          ))
        )}

        {sending && (
          <div className="mr-auto max-w-[90%] rounded border bg-white p-3 text-sm">
            <p className="mb-1 text-xs text-gray-500">DevLens</p>
            <p className="text-gray-500">Thinking...</p>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {error && (
        <p className="rounded bg-red-50 p-2 text-sm text-red-600">{error}</p>
      )}

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about this repository..."
          className="flex-1 rounded border px-3 py-2"
        />

        <button
          type="submit"
          disabled={sending || !input.trim()}
          className="rounded bg-black px-4 py-2 text-white disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </section>
  );
}