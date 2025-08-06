import type { Metadata } from "next";
import "./globals.css";
import ThemeRegistry from "./ThemeRegistry";
import { AuthProvider } from "@/context/AuthContext";
import QueryProvider from "./QueryProvider";
import { NotificationProvider } from "@/context/NotificationContext";

export const metadata: Metadata = {
  title: "Paasell",
  description: "Paasell",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <ThemeRegistry>
          <AuthProvider>
            <QueryProvider>
              <NotificationProvider>
                {children}
              </NotificationProvider>
            </QueryProvider>
          </AuthProvider>
        </ThemeRegistry>
      </body>
    </html>
  );
}
