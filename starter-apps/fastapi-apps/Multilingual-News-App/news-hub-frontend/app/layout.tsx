import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Global News Hub - Multilingual News Platform",
  description: "Get the latest news from around the world in 50+ languages. Powered by AI translation.",
  keywords: "news, global news, multilingual, translation, AI, world news",
  authors: [{ name: "Global News Hub Team" }],
  openGraph: {
    title: "Global News Hub",
    description: "Get the latest news from around the world in 50+ languages",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}
