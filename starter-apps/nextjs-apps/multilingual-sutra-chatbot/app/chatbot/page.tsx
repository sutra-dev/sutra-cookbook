import { Suspense } from "react";
import ChatbotClient from "./ChatbotClient";

export default function ChatbotPage() {
    return (
        <Suspense fallback={<div className="p-6">Loading chatbot...</div>}>
            <ChatbotClient />
        </Suspense>
    );
}
