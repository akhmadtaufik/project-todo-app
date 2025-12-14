"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/axios";
import { Button } from "@/components/ui/button";
import { LogOut, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { motion } from "framer-motion";

interface DecodedToken {
  sub: string;
  exp: number;
}

interface User {
  id: string;
  name: string;
  email: string;
}

export default function Dashboard() {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/auth");
      return;
    }

    try {
      const decoded = jwtDecode<DecodedToken>(token);
      setUserId(decoded.sub);
    } catch (error) {
      console.error("Invalid token", error);
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      router.push("/auth");
    }
  }, [router]);

  const { data: user, isLoading, isError } = useQuery({
    queryKey: ["user", userId],
    queryFn: async () => {
      if (!userId) return null;
      // Backend expects Bearer token (handled by interceptor)
      const res = await api.get(`/api/users/${userId}`);
      return res.data;
    },
    enabled: !!userId, // Only run when userId is known
  });

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    toast.success("Logged out successfully");
    router.push("/auth");
  };

  if (isLoading || !userId) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (isError) {
     return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50">
           <p className="text-rose-600 mb-4">Failed to load user data.</p>
           <Button onClick={handleLogout} variant="outline">Back to Login</Button>
        </div>
     )
  }

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      {/* Navbar Placeholder */}
      <nav className="flex justify-between items-center mb-16 max-w-5xl mx-auto">
         <div className="font-bold text-xl tracking-tight text-slate-900">Antigravity</div>
         <Button onClick={handleLogout} variant="ghost" className="text-slate-500 hover:text-rose-600 hover:bg-rose-50">
            <LogOut className="h-4 w-4 mr-2" /> Logout
         </Button>
      </nav>

      {/* Hero / Greeting */}
      <main className="max-w-5xl mx-auto">
        <motion.div
           initial={{ opacity: 0, y: 20 }}
           animate={{ opacity: 1, y: 0 }}
           transition={{ duration: 0.6 }}
        >
            <h1 className="text-4xl md:text-5xl font-bold text-slate-900 leading-tight">
               Welcome back, <span className="text-blue-600">{user?.name}</span>.
            </h1>
            <p className="text-xl text-slate-500 mt-4 max-w-2xl font-light">
               You are all caught up. Ready to enter the flow state?
            </p>
        </motion.div>

        {/* Placeholder Content */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
            {[1, 2, 3].map((i) => (
                <motion.div 
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 + (i * 0.1) }}
                    className="h-48 bg-white rounded-xl border border-slate-100 shadow-sm p-6 hover:shadow-md transition-shadow"
                >
                   <div className="h-8 w-8 bg-slate-100 rounded-full mb-4"></div>
                   <div className="h-4 w-2/3 bg-slate-100 rounded mb-2"></div>
                   <div className="h-3 w-1/2 bg-slate-50 rounded"></div>
                </motion.div>
            ))}
        </div>
      </main>
    </div>
  );
}
