"use client";

import { useEffect, useRef, useState } from "react";
import { ChevronDown } from "lucide-react";

interface SelectDropdownProps {
    label: string;
    value: string;
    options: string[];
    onChange: (val: string) => void;
}

export default function SelectDropdown({
    label,
    value,
    options,
    onChange,
}: SelectDropdownProps) {
    const [open, setOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

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
        <div className="w-full relative" ref={dropdownRef}>
            <label className="block mb-2 text-sm font-semibold text-blue-900">
                {label}:
            </label>

            <button
                type="button"
                onClick={() => setOpen((prev) => !prev)}
                className="w-full px-4 py-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:to-indigo-700 text-white/90 font-semibold shadow-sm transition flex items-center justify-between"
            >
                <span>{value || `Select ${label}`}</span>
                <ChevronDown size={18} />
            </button>


            {open && (
                <div className="absolute z-30 mt-2 w-full rounded-xl border border-blue-200 bg-white dark:bg-white shadow-2xl p-2 flex flex-col animate-fade-in">
                    {options.map((option) => (
                        <button
                            key={option}
                            type="button"
                            onClick={() => {
                                onChange(option);
                                setOpen(false);
                            }}
                            className={`font-semibold text-left w-full px-3 py-2 rounded-md text-sm text-zinc-800 dark:text-black/60 hover:bg-blue-600 hover:text-white/70 transition ${option === value ? "bg-indigo-00" : ""
                                }`}
                        >
                            {option}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
