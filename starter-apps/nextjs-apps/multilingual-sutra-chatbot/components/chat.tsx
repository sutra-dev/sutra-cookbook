"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import ApiKeyInput from "./api-key-input";
import LanguageDropdown from "./language-dropdown";
import SelectDropdown from "./select-dropdown";
import { TONES, LENGTHS, CONTENT_TYPES } from "../constants";
import { ChevronRight } from "lucide-react";

export default function StreamChat() {
    const router = useRouter();

    const [languages, setLanguages] = useState<string[]>(["English"]);
    const [tone, setTone] = useState("Formal");
    const [length, setLength] = useState("Medium");
    const [contentType, setContentType] = useState("Blog");
    const [apiKey, setApiKey] = useState("");
    const [isVerifying, setIsVerifying] = useState(false);
    const [isVerified, setIsVerified] = useState(false);
    const [verificationError, setVerificationError] = useState("");

    const handleVerifyApiKey = async () => {
        setIsVerifying(true);
        setVerificationError("");
        try {
            const res = await fetch("/api/verify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ apiKey }),
            });

            if (res.ok) {
                setIsVerified(true);
            } else {
                setVerificationError("Invalid API Key. Please try again.");
                setIsVerified(false);
            }
        } catch {
            setVerificationError("Error verifying API Key.");
            setIsVerified(false);
        } finally {
            setIsVerifying(false);
        }
    };

    const handleGoToChatbot = () => {
        const query = new URLSearchParams({
            apiKey,
            isVerified: String(isVerified),
            languages: languages.join(","),
            tone,
            length,
            contentType,
        }).toString();

        router.push(`/chatbot?${query}`);
    };

    return (
        <div className="max-w-3xl mx-auto px-6 py-8 mt-8 rounded-3xl bg-white/80 border border-slate-300 shadow-xl space-y-8 transition-colors">
            <h1 className="text-3xl font-semibold text-center dark:text-blue-800 drop-shadow">
                SUTRA Chat Configuration
            </h1>

            {/* API Key */}
            <div className="px-4 py-2 flex justify-end">
                <ApiKeyInput
                    apiKey={apiKey}
                    setApiKey={(key) => {
                        setApiKey(key);
                        setIsVerified(false);
                    }}
                    onVerify={handleVerifyApiKey}
                    isVerified={isVerified}
                    isVerifying={isVerifying}
                    error={verificationError}
                />
            </div>

            {/* Dropdowns */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-6">
                    <label className="text-blue-900 text-sm font-semibold">Languages:</label>
                    <LanguageDropdown selected={languages} setSelected={setLanguages} />
                </div>
                <SelectDropdown label="Tone" value={tone} options={TONES} onChange={setTone} />
                <SelectDropdown label="Length" value={length} options={LENGTHS} onChange={setLength} />
                <SelectDropdown label="Content Type" value={contentType} options={CONTENT_TYPES} onChange={setContentType} />
            </div>

            <div className="text-sm text-blue-600 dark:text-blue-900 italic text-center">
                Responding in: <strong>{languages.join(", ")}</strong> | Tone: <strong>{tone}</strong> | Length:{" "}
                <strong>{length}</strong> | Type: <strong>{contentType}</strong>
            </div>

            <div className="flex justify-center">
                <button
                    onClick={handleGoToChatbot}
                    disabled={!isVerified}
                    className="px-6 py-2 mt-4 bg-gradient-to-r gap-3 items-center flex from-blue-600 to-indigo-600 hover:to-indigo-700 text-white/95 font-semibold rounded-xl shadow-lg transition disabled:opacity-50"
                >
                    Go to Chatbot <ChevronRight size={18} />
                </button>
            </div>
        </div>
    );
}
