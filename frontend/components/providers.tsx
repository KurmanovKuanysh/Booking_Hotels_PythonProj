"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";
import { useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: { staleTime: 1000 * 60, retry: 1 },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: "#1A1410",
            color: "#F5F0E8",
            border: "1px solid #52483E",
            fontFamily: "'DM Sans', sans-serif",
            fontSize: "14px",
          },
          success: {
            iconTheme: { primary: "#C9A84C", secondary: "#1A1410" },
          },
        }}
      />
    </QueryClientProvider>
  );
}
