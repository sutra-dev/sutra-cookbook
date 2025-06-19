"use client";

import { useEffect, useRef, useState } from "react";
import { ChevronDown } from "lucide-react";

export const ALL_LANGUAGES = [
    "English",
    "Hindi",
    "Spanish",
    "French",
    "German",
    "Chinese",
    "Japanese",
];

interface LanguageDropdownProps {
    selected: string[];
    setSelected: (langs: string[]) => void;
}

export default function LanguageDropdown({
    selected,
    setSelected,
}: LanguageDropdownProps) {
    const [open, setOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    const toggleLanguage = (lang: string) => {
        setSelected(
            selected.includes(lang)
                ? selected.filter((l) => l !== lang)
                : [...selected, lang]
        );
    };

    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (
                dropdownRef.current &&
                !dropdownRef.current.contains(e.target as Node)
            ) {
                setOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () =>
            document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    return (
        <div className="relative w-full" ref={dropdownRef}>
            <button
                type="button"
                onClick={() => setOpen((prev) => !prev)}
                className="text-left h-10 w-full px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:to-indigo-700 text-sm font-semibold text-white/90 shadow-md transition flex items-center justify-between focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
                {selected.length > 0 ? (
                    <span className="truncate">Selected: {selected.join(", ")}</span>
                ) : (
                    <span>Select Languages</span>
                )}
                <ChevronDown size={18} className="ml-2 text-white" />
            </button>


            {open && (
                <div className="absolute z-30 mt-2 w-full rounded-xl border border-blue-200 bg-white dark:bg-white shadow-2xl p-4 grid grid-cols-2 gap-3 animate-fade-in">
                    {ALL_LANGUAGES.map((lang) => (
                        <label
                            key={lang}
                            className="flex items-center gap-2 text-sm text-zinc-700 dark:text-black/60 font-semibold"
                        >
                            <input
                                type="checkbox"
                                checked={selected.includes(lang)}
                                onChange={() => toggleLanguage(lang)}
                                className="accent-blue-500 w-4 h-4 rounded focus:ring-2 focus:ring-blue-400"
                            />
                            <span>{lang}</span>
                        </label>
                    ))}
                </div>
            )}
        </div>
    );
}
