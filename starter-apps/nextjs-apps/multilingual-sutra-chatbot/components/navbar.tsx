import React from "react";
import Link from "next/link";
import Image from "next/image";

export default function Navbar() {
    return (
        <div className="relative z-50 flex items-center justify-between px-6 py-6">
            <Link href="/" className="flex items-center">
                <Image
                    src="/logo-.png"
                    alt="Logo"
                    width={150}
                    height={40}
                    priority
                />
            </Link>

            <div className="absolute right-80 top-1/2 -translate-y-1/2">
                <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full transition-all bg-red-50 text-red-600 border border-red-200">
                    <span className="inline-block w-2 h-2 bg-red-500 rounded-full"></span>
                    <span className="text-sm font-medium">Sutra API</span>
                </div>
            </div>

        </div>

    );
}
