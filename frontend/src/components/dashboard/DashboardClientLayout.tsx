"use client";

import { useState } from "react";
import { Sidebar } from "@/components/dashboard/Sidebar";
import { Topbar } from "@/components/dashboard/Topbar";
import { PageTransition } from "@/components/dashboard/PageTransition";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function DashboardClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-slate-50/50">
      {/* Desktop Sidebar - hidden on mobile */}
      <div className="hidden md:flex flex-col w-64 fixed inset-y-0 z-50">
         <Sidebar />
      </div>

      {/* Mobile Sidebar Overlay */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-50 flex md:hidden">
            {/* Backdrop */}
            <div 
                className="fixed inset-0 bg-black/50 backdrop-blur-sm"
                onClick={() => setIsMobileMenuOpen(false)}
            />
            {/* Sidebar Pane */}
            <div className="relative flex flex-col w-64 h-full bg-white shadow-xl animate-in slide-in-from-left duration-200">
                <Button 
                    variant="ghost" 
                    size="icon" 
                    className="absolute top-4 right-4 z-50"
                    onClick={() => setIsMobileMenuOpen(false)}
                >
                    <X className="w-5 h-5" />
                </Button>
                <Sidebar className="border-none shadow-none" />
            </div>
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col md:pl-64 transition-all duration-300">
        <Topbar onMobileMenuClick={() => setIsMobileMenuOpen(true)} />
        
        <main className="flex-1 p-6 overflow-x-hidden">
             <PageTransition>
                {children}
             </PageTransition>
        </main>
      </div>
    </div>
  );
}
