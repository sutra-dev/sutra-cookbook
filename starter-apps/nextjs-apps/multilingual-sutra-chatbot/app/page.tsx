// app/page.tsx
"use client";

import Chat from '@/components/chat';
import Navbar from '@/components/navbar';

export default function Page() {

  return (
    <div className="flex flex-col px-4 py-8">
      <Navbar />

      <div className="flex flex-col items-center">
        <h1 className="font-semibold text-5xl mb-4 text-center">
          Multilingual
          <span className="text-blue-600"> Content Generation</span>
        </h1>

        <p className="text-center max-w-xl text-black/60">
          Create your content in different forms across multiple languages
        </p>

        <div className="mt-10 w-full max-w-3xl rounded-3xl">
          <Chat />
        </div>
      </div>
    </div>

  );
}
