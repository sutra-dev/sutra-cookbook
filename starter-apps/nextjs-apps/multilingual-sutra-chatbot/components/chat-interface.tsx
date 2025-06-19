"use client";

import React, { useRef, useEffect, useState } from "react";
import { useChat } from "ai/react";
import ReactMarkdown from "react-markdown";

interface ChatInterfaceProps {
    apiKey: string;
    isVerified: boolean;
    languages: string[];
    tone: string;
    length: string;
    contentType: string;
}

export default function ChatInterface({
    apiKey,
    isVerified,
    languages,
    tone,
    length,
    contentType,
}: ChatInterfaceProps) {
    const [localMessages, setLocalMessages] = useState<string[]>([]);

    const {
        messages,
        input,
        handleInputChange,
        handleSubmit: baseSubmit,
    } = useChat({
        api: "/api/chat",
        body: { languages, tone, length, contentType, apiKey },
        key: `${languages.join(",")}-${tone}-${length}-${contentType}-${apiKey}`,
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!apiKey) {
            alert("Please enter your Sutra API key.");
            return;
        }
        baseSubmit(e);
    };

    const handleRemoveUserMessage = (id: string) => {
        const index = messages.findIndex((m) => m.id === id);
        if (index === -1) return;

        const toRemove = [messages[index].id];
        if (messages[index + 1]?.role === "assistant") {
            toRemove.push(messages[index + 1].id);
        }
        setLocalMessages((prev) => [...prev, ...toRemove]);
    };

    const visibleMessages = messages.filter((m) => !localMessages.includes(m.id));

    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    return (
        <>
            {/* Summary */}
            <div className="text-sm text-blue-600 dark:text-blue-900 italic">
                Responding in: <strong>{languages.join(", ")}</strong> | Tone: <strong>{tone}</strong> | Length:{" "}
                <strong>{length}</strong> | Type: <strong>{contentType}</strong>
            </div>

            {/* Message Input */}
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4">
                <input
                    disabled={!isVerified}
                    value={input}
                    onChange={handleInputChange}
                    placeholder="Ask SUTRA-V2 something..."
                    className="flex-1 p-3 rounded-lg bg-white text-gray-800 dark:bg-blue-900/40 dark:text-white border border-blue-200 dark:border-blue-700 placeholder:text-gray-500 dark:placeholder:text-white/60 transition"
                />
                <button
                    type="submit"
                    disabled={!isVerified || !input.trim()}
                    className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition font-semibold shadow-md disabled:opacity-50"
                >
                    Send
                </button>
            </form>

            {/* Messages */}
            <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                {visibleMessages.map((m) => (
                    <div
                        key={m.id}
                        className={`relative p-4 rounded-xl border transition ${m.role === "user"
                            ? "bg-white dark:bg-blue-950 border-blue-100 dark:border-blue-800"
                            : "bg-blue-100/30 dark:bg-emerald-900/20 border border-blue-300 dark:border-emerald-600"
                            }`}
                    >
                        {m.role === "user" && (
                            <button
                                onClick={() => handleRemoveUserMessage(m.id)}
                                className="absolute top-2 right-3 text-gray-400 hover:text-red-500 text-xl font-bold"
                                aria-label="Remove message"
                            >
                                ×
                            </button>
                        )}
                        <span className="block mb-2 font-semibold capitalize text-sm text-blue-900 dark:text-blue-200">
                            {m.role}
                        </span>
                        <div className="prose prose-sm dark:prose-invert max-w-none whitespace-pre-wrap">
                            <ReactMarkdown>{m.content}</ReactMarkdown>
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
        </>
    );
}
