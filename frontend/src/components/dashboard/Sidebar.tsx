"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LayoutDashboard, FolderKanban, Calendar, LogOut, Plus, RefreshCw } from "lucide-react";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { getProjects } from "@/services/project.service";
import type { Project } from "@/types";
import api from "@/lib/axios";

interface User {
  name: string;
  email: string;
}

// Skeleton loader for project list items
function ProjectSkeleton() {
  return (
    <div className="space-y-1">
      {[1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          className="flex items-center gap-3 px-3 py-2 animate-pulse"
        >
          <div className="w-2 h-2 rounded-full bg-slate-200" />
          <div className="h-4 flex-1 bg-slate-200 rounded" />
        </div>
      ))}
    </div>
  );
}

export function Sidebar({ className }: { className?: string }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<User | null>({ name: "Demo User", email: "demo@example.com" });

  // Fetch projects using TanStack Query
  const {
    data: projects = [],
    isLoading,
    isError,
    refetch,
  } = useQuery({
    queryKey: ["sidebar-projects"],
    queryFn: () => getProjects({ limit: 5 }),
    staleTime: 1000 * 60 * 5, // 5 minutes
    refetchOnWindowFocus: false,
    retry: 1,
  });

  const handleLogout = async () => {
    try {
      await api.post("/api/auth/logout");
      localStorage.removeItem("access_token");
      router.push("/auth");
    } catch (error) {
      console.error("Logout failed", error);
      router.push("/auth");
    }
  };

  const links = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/dashboard/projects", label: "All Projects", icon: FolderKanban },
    { href: "/dashboard/calendar", label: "Calendar", icon: Calendar },
  ];

  // Render project list content based on state
  const renderProjectList = () => {
    if (isLoading) {
      return <ProjectSkeleton />;
    }

    if (isError) {
      return (
        <div className="flex items-center gap-2 px-3 py-2 text-sm text-slate-500">
          <span className="flex-1 text-xs">Could not load projects</span>
          <button
            onClick={() => refetch()}
            className="text-slate-400 hover:text-indigo-600 transition-colors p-1"
            aria-label="Retry loading projects"
          >
            <RefreshCw className="w-3 h-3" />
          </button>
        </div>
      );
    }

    if (projects.length === 0) {
      return (
        <div className="flex items-center gap-2 px-3 py-2 text-sm text-slate-400">
          <span className="flex-1">No projects yet</span>
          <Link
            href="/dashboard/projects/new"
            className="text-slate-400 hover:text-indigo-600 transition-colors p-1"
            aria-label="Create new project"
          >
            <Plus className="w-3.5 h-3.5" />
          </Link>
        </div>
      );
    }

    return projects.map((project: Project) => (
      <Link
        key={project.project_id}
        href={`/dashboard/projects/${project.project_id}`}
        className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors"
      >
        <span
          className="w-2 h-2 rounded-full"
          style={{ backgroundColor: "#6366f1" }}
        />
        {project.project_name}
      </Link>
    ));
  };

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
             <Link
               href="/dashboard/projects/new"
               className="text-slate-400 hover:text-indigo-600 transition-colors"
             >
                <Plus className="w-3 h-3" />
             </Link>
          </div>
          
          {renderProjectList()}
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
