"use client";

import { useChat } from "ai/react";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import { ArrowLeft, MessageSquare } from "lucide-react";
import Link from "next/link";

export default function ChatbotClient() {
    const searchParams = useSearchParams();

    const languages = searchParams.get("languages")?.split(",") || ["English"];
    const tone = searchParams.get("tone") || "Formal";
    const length = searchParams.get("length") || "Medium";
    const contentType = searchParams.get("contentType") || "Blog";
    const apiKey = searchParams.get("apiKey") || "";
    const isVerified = searchParams.get("isVerified") === "true";

    const [localMessages, setLocalMessages] = useState<string[]>([]);
    const bottomRef = useRef<HTMLDivElement>(null);

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
            alert("API key missing.");
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

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [visibleMessages]);

    return (
        <div className="min-h-screen flex flex-col bg-blue-50 text-blue-950 relative">
            {/* Header */}
            <header className="bg-white/70 shadow-sm backdrop-blur-sm px-4 py-3 flex items-center justify-between">
                <div className="flex items-center gap-1">
                    <Link
                        href="/"
                        aria-label="Back to home"
                        className="inline-flex items-center justify-center size-9 rounded-full text-blue-700 hover:bg-blue-100 transition"
                    >
                        <ArrowLeft size={20} />
                    </Link>
                    <Link
                        href="/"
                        className="text-blue-950 font-semibold hover:underline"
                    >
                        Reconfigure
                    </Link>
                </div>
            </header>

            {/* Message Area */}
            <main className="flex-1 overflow-y-auto px-4 sm:px-6 py-6 space-y-4 pb-32">
                <div className="space-y-4 max-w-3xl mx-auto">
                    {visibleMessages.length === 0 ? (
                        <div
                            className="flex-1 overflow-y-auto p-4 space-y-3"
                            style={{
                                backgroundImage:
                                    "radial-gradient(circle at 1rem 1rem, rgba(224, 231, 255, 0.15) 1rem, transparent 1rem)",
                                backgroundSize: "3rem 3rem",
                            }}
                        >
                            <div className="h-full flex flex-col items-center justify-center text-center p-6">
                                <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
                                    <MessageSquare className="h-8 w-8 text-indigo-600" />
                                </div>
                                <h3 className="text-lg font-semibold text-slate-800">No messages yet</h3>
                                <p className="text-slate-500 max-w-sm mt-1">
                                    Start the conversation by sending your first message below.
                                </p>
                            </div>
                        </div>
                    ) : (
                        visibleMessages.map((m) => (
                            <div
                                key={m.id}
                                className={`relative p-4 rounded-xl border transition ${m.role === "user"
                                    ? "bg-white border-blue-100"
                                    : "bg-white border-blue-300"
                                    }`}
                            >
                                {m.role === "user" && (
                                    <button
                                        onClick={() => handleRemoveUserMessage(m.id)}
                                        className="absolute top-2 right-3 text-blue-400 hover:text-red-500 text-xl font-bold"
                                        aria-label="Remove message"
                                    >
                                        ×
                                    </button>
                                )}
                                <span className="block mb-2 font-semibold capitalize text-sm text-blue-800">
                                    {m.role}
                                </span>
                                <div className="prose prose-sm max-w-none whitespace-pre-wrap">
                                    <ReactMarkdown>{m.content}</ReactMarkdown>
                                </div>
                            </div>
                        ))
                    )}

                    <div ref={bottomRef} />
                </div>
            </main>

            {/* Input Footer */}
            <footer className="fixed bottom-0 left-0 w-full border-t border-blue-200 bg-white/80 backdrop-blur-md px-4 sm:px-6 py-4 z-10">
                <form
                    onSubmit={handleSubmit}
                    className="flex flex-col sm:flex-row gap-4 max-w-3xl mx-auto"
                >
                    <input
                        disabled={!isVerified}
                        value={input}
                        onChange={handleInputChange}
                        placeholder="Ask SUTRA-V2 something..."
                        className="flex-1 p-3 rounded-3xl bg-white scroll-smooth text-blue-950 border border-blue-300 placeholder:text-black/60 focus:outline-none focus:ring-0 focus:border-blue-300 focus:border-2 transition"
                    />
                    <button
                        type="submit"
                        disabled={!isVerified}
                        className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-3xl transition font-semibold shadow-md disabled:opacity-50"
                    >
                        Send
                    </button>
                </form>
            </footer>
        </div>
    );
}
