"use client";

import { usePathname } from "next/navigation";
import { Search, ChevronRight, Bell, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import React from "react";

interface TopbarProps {
  onMobileMenuClick?: () => void;
}

export function Topbar({ onMobileMenuClick }: TopbarProps) {
  const pathname = usePathname();
  
  // Generate breadcrumbs from pathname
  const segments = pathname.split('/').filter(Boolean);
  const breadcrumbs = segments.map((segment, index) => {
    const href = `/${segments.slice(0, index + 1).join('/')}`;
    const label = segment.charAt(0).toUpperCase() + segment.slice(1);
    const isLast = index === segments.length - 1;
    return { href, label, isLast };
  });

  const [formattedDate, setFormattedDate] = React.useState("");

  React.useEffect(() => {
    setFormattedDate(new Date().toLocaleDateString("en-US", {
      weekday: "short",
      day: "numeric",
      month: "short",
    }));
  }, []);

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b border-white/20 bg-white/30 backdrop-blur-md px-6 shadow-sm">
      {/* Mobile Menu Button */}
      <Button 
        variant="ghost" 
        size="icon" 
        className="md:hidden mr-2 -ml-2"
        onClick={onMobileMenuClick}
      >
        <Menu className="w-5 h-5" />
      </Button>

      <div className="flex-1 flex items-center gap-4">
        {/* Breadcrumbs */}
        <nav className="flex items-center text-sm font-medium text-slate-500">
          <Link href="/dashboard" className="hover:text-slate-900 transition-colors">
            Home
          </Link>
          {breadcrumbs.length > 0 && breadcrumbs.map((crumb) => (
             <React.Fragment key={crumb.href}>
                <ChevronRight className="w-4 h-4 mx-1 text-slate-400" />
                {crumb.isLast ? (
                    <span className="text-slate-900 font-semibold cursor-default">
                        {crumb.label}
                    </span>
                ) : (
                    <Link href={crumb.href} className="hover:text-slate-900 transition-colors">
                        {crumb.label}
                    </Link>
                )}
             </React.Fragment>
          ))}
        </nav>
      </div>

      <div className="flex items-center gap-4">
        {/* Search */}
        <div className="relative w-64 hidden md:block">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-500" />
            <Input 
                type="search" 
                placeholder="Search..." 
                className="w-full bg-slate-50/50 border-0 focus-visible:ring-indigo-500 pl-9 rounded-full shadow-inner"
            />
        </div>

        {/* Date Display */}
        <div className="hidden md:flex flex-col items-end mr-2">
            <span className="text-xs font-semibold text-slate-500 uppercase">Today</span>
            <span className="text-sm font-medium text-slate-900 min-h-[20px]">{formattedDate}</span>
        </div>
        
        <Button variant="ghost" size="icon" className="text-slate-500 hover:text-indigo-600 rounded-full">
            <Bell className="w-5 h-5" />
        </Button>
      </div>
    </header>
  );
}
