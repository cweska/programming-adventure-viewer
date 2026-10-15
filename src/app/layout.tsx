import type { Metadata } from "next";
import { Fraunces, IBM_Plex_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const display = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
});

const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "Emberkeep Lesson Theater",
  description: "A dungeon lesson theater for Python.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${mono.variable}`}>
        <header className="site-header">
          <p className="wordmark">Emberkeep</p>
          <nav className="site-nav" aria-label="Site">
            <Link href="/">Play</Link>
            <Link href="/author">Author</Link>
            <Link href="/classroom">Classroom</Link>
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
