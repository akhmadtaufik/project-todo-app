"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LayoutDashboard, FolderKanban, Calendar, LogOut, Plus } from "lucide-react";
import { useEffect, useState } from "react";
import axios from "axios";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface Project {
  _id: string;
  name: string;
  color?: string;
}

interface User {
  name: string;
  email: string;
}

export function Sidebar({ className }: { className?: string }) {
  const pathname = usePathname();
  const router = useRouter();
  const [projects, setProjects] = useState<Project[]>([]);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Mock user for now if API fails or is not ready
    // intended: GET /api/users/me
    const fetchUser = async () => {
        try {
            // Placeholder: Replace with actual API call
             // const { data } = await axios.get("/api/users/me");
             // setUser(data);
             setUser({ name: "Demo User", email: "demo@example.com" });
        } catch (error) {
            console.error("Failed to fetch user", error);
        }
    };
    
    // intended: GET /api/projects?limit=5
    const fetchProjects = async () => {
      try {
        // Placeholder: Replace with actual API call
        // const { data } = await axios.get("/api/projects?limit=5");
        // setProjects(data);
        setProjects([
            { _id: "1", name: "Website Redesign", color: "#3b82f6" },
            { _id: "2", name: "Mobile App", color: "#10b981" },
            { _id: "3", name: "Audit Logs", color: "#f59e0b" },
        ]);
      } catch (error) {
        console.error("Failed to fetch projects", error);
      }
    };

    fetchUser();
    fetchProjects();
  }, []);

  const handleLogout = async () => {
    try {
      await axios.post("/api/auth/logout");
      // Clear local storage if token stored there
      localStorage.removeItem("token"); 
      router.push("/auth");
    } catch (error) {
      console.error("Logout failed", error);
      // Force redirect anyway
      router.push("/auth");
    }
  };

  const links = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/dashboard/projects", label: "All Projects", icon: FolderKanban },
    { href: "/dashboard/calendar", label: "Calendar", icon: Calendar },
  ];

  return (
    <aside className={cn("flex flex-col h-full border-r border-white/20 bg-white/30 backdrop-blur-md shadow-sm w-64 transition-all duration-300", className)}>
      <div className="p-6">
        <h1 className="text-xl font-bold tracking-tight text-slate-800 flex items-center gap-2">
            <span className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-sm">AG</span>
            Antigravity
        </h1>
      </div>

      <nav className="flex-1 px-4 space-y-6 overflow-y-auto">
        {/* Main Navigation */}
        <div className="space-y-1">
          <p className="px-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Platform</p>
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors",
                  isActive
                    ? "bg-slate-900/5 text-slate-900"
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                )}
              >
                <Icon className="w-4 h-4" />
                {link.label}
              </Link>
            );
          })}
        </div>

        {/* Quick Projects */}
        <div className="space-y-1">
          <div className="flex items-center justify-between px-2 mb-2">
             <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Quick Projects</p>
             <button className="text-slate-400 hover:text-indigo-600 transition-colors">
                <Plus className="w-3 h-3" />
             </button>
          </div>
          
          {projects.length === 0 ? (
            <div className="px-3 text-sm text-slate-400">No recent projects</div>
          ) : (
            projects.map((project) => (
              <Link
                key={project._id}
                href={`/dashboard/projects/${project._id}`}
                className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors"
              >
                <span 
                    className="w-2 h-2 rounded-full" 
                    style={{ backgroundColor: project.color || "#cbd5e1" }}
                />
                {project.name}
              </Link>
            ))
          )}
        </div>
      </nav>

      {/* User Actions */}
      <div className="p-4 border-t border-white/20">
        <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-xs font-bold text-slate-600">
                {user?.name?.[0] || "U"}
            </div>
            <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-slate-900 truncate">{user?.name || "Loading..."}</p>
                <p className="text-xs text-slate-500 truncate">{user?.email}</p>
            </div>
        </div>
        <Button 
            variant="ghost" 
            className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50 gap-2"
            onClick={handleLogout}
        >
            <LogOut className="w-4 h-4" />
            Sign Out
        </Button>
      </div>
    </aside>
  );
}
