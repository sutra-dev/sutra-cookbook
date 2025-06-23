"use client";

import { useState } from "react";
import { Key, X, ChevronRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function ApiKeyInput({
    apiKey,
    setApiKey,
    onVerify,
    isVerified,
    isVerifying,
    error,
}: {
    apiKey: string;
    setApiKey: (key: string) => void;
    onVerify: () => void;
    isVerified: boolean;
    isVerifying: boolean;
    error: string;
}) {
    const [showModal, setShowModal] = useState(false);

    return (
        <>
            <button
                type="button"
                onClick={() => setShowModal(true)}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-blue-50 hover:bg-blue-100 text-blue-800 border border-blue-200 rounded-lg transition-all shadow-sm"
            >
                <Key size={16} />
                Configure API Key
            </button>

            <AnimatePresence>
                {showModal && (
                    <>
                        {/* Darker Backdrop with more opacity */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm"
                            onClick={() => setShowModal(false)}
                        />

                        {/* Modal content */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            transition={{ duration: 0.25 }}
                            className="fixed z-50 top-1/2 left-1/2 w-[95%] max-w-lg -translate-x-1/2 -translate-y-1/2 bg-white dark:bg-white border border-zinc-200 dark:border-blue-700 rounded-3xl shadow-2xl p-8 space-y-6"
                        >
                            <div className="flex justify-between items-center">
                                <h2 className="text-xl font-semibold text-blue-800 dark:text-blue-900">
                                    Enter Your Sutra API Key
                                </h2>
                                <button
                                    onClick={() => setShowModal(false)}
                                    className="text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-300"
                                >
                                    <X size={22} />
                                </button>
                            </div>

                            <div className="space-y-3">
                                <label className="text-base font-medium text-black/70 block">
                                    API Key
                                </label>
                                <div className="flex flex-col items-center gap-5">
                                    <input
                                        type="password"
                                        value={apiKey}
                                        onChange={(e) => setApiKey(e.target.value)}
                                        placeholder="Enter your API key"
                                        className="w-full px-4 py-3 text-base border-2 border-blue-300 rounded-lg bg-white text-black/80 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                                    /> <button
                                        type="button"
                                        onClick={async () => {
                                            await onVerify();
                                            if (!isVerifying && !error) {
                                                setShowModal(false);
                                            }
                                        }}
                                        disabled={isVerifying || !apiKey}
                                        className={`w-full rounded-xl px-5 py-3 text-base font-semibold transition text-white flex items-center justify-center gap-2 ${isVerifying
                                            ? "bg-blue-400 cursor-not-allowed"
                                            : "bg-blue-600 hover:bg-blue-700"
                                            }`}
                                    >
                                        {isVerifying ? (
                                            "Verifying..."
                                        ) : (
                                            <>
                                                Continue to Chat
                                                <ChevronRight size={18} />
                                            </>
                                        )}
                                    </button>

                                </div>

                                {!isVerified && !isVerifying && (
                                    <p className="text-sm text-black/60">
                                        {error || (
                                            <>
                                                No API key?{" "}
                                                <a
                                                    href="https://www.two.ai/sutra/api"
                                                    target="_blank"
                                                    className="underline font-medium text-blue-600 hover:text-blue-800"
                                                    rel="noopener noreferrer"
                                                >
                                                    Get your key here
                                                </a>
                                            </>
                                        )}
                                    </p>
                                )}
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
    );
}
