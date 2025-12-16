"use client";

import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import { toast } from "sonner";
import { DashboardSkeleton } from "@/components/dashboard/DashboardSkeleton";
import { GreetingSection } from "@/components/dashboard/GreetingSection";
import { ProjectSummaryCard } from "@/components/dashboard/ProjectSummaryCard";
import { TaskOverview } from "@/components/dashboard/TaskOverview";
import { ErrorState } from "@/components/dashboard/ErrorState";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import { getProjects } from "@/services/project.service";
import type { Project, Task, User } from "@/types";
import api from "@/lib/axios";

/**
 * Check if a date string matches today's date
 */
function isToday(dateStr: string | undefined): boolean {
  if (!dateStr) return false;
  const today = new Date().toISOString().split("T")[0];
  return dateStr.startsWith(today);
}

/**
 * Calculate project progress percentage
 */
function calculateProgress(tasks: Task[]): number {
  if (tasks.length === 0) return 0;
  const completed = tasks.filter((t) => t.status === "Completed").length;
  return Math.round((completed / tasks.length) * 100);
}

/**
 * Get count of completed tasks
 */
function getCompletedCount(tasks: Task[]): number {
  return tasks.filter((t) => t.status === "Completed").length;
}

export default function DashboardPage() {
  const router = useRouter();

  // Auth check
  useEffect(() => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        router.push("/auth");
        return;
      }
      jwtDecode(token);
    } catch {
      router.push("/auth");
    }
  }, [router]);

  // Fetch user data
  const { data: user } = useQuery<User>({
    queryKey: ["user"],
    queryFn: async () => {
      const { data } = await api.get<User>("/api/users/me");
      return data;
    },
    staleTime: 1000 * 60 * 5,
    refetchOnWindowFocus: false,
    retry: 1,
  });

  // Fetch projects with nested tasks - single query, no waterfall
  const {
    data: projects = [],
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ["dashboard-projects"],
    queryFn: () => getProjects({ limit: 10 }),
    staleTime: 1000 * 60 * 5, // 5 minutes
    refetchOnWindowFocus: false,
    retry: 1,
  });

  // Show toast on error
  useEffect(() => {
    if (isError) {
      toast.error("Failed to sync dashboard", {
        description: error instanceof Error ? error.message : "Please check your connection",
      });
    }
  }, [isError, error]);

  // --- Computed Values ---

  // Flatten all tasks from all projects
  const allTasks: Task[] = projects.flatMap((p: Project) => p.task || []);

  // Tasks due today (not completed)
  const tasksDueToday = allTasks.filter(
    (t) => isToday(t.due_date) && t.status !== "Completed"
  );

  // In-progress tasks (not already in tasksDueToday)
  const inProgressTasks = allTasks.filter(
    (t) => t.status === "In Progress" && !tasksDueToday.includes(t)
  );

  // Tasks for TaskOverview component (combine due today + in progress)
  const overviewTasks = [...tasksDueToday, ...inProgressTasks].slice(0, 8);

  // Top 3 projects for summary cards
  const topProjects = projects.slice(0, 3);

  // --- Render ---

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (isError) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center animate-in fade-in duration-500">
        <ErrorState
          title="Connection Lost"
          message="We couldn't load your dashboard. Please check your server connection and try again."
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <GreetingSection
        userName={user?.name || "User"}
        pendingTasksCount={tasksDueToday.length}
      />

      {/* Projects Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-slate-900">Active Projects</h2>
          <Button
            size="sm"
            className="bg-indigo-600 hover:bg-indigo-700 text-white gap-2 shadow-indigo-200 shadow-md"
          >
            <Plus className="w-4 h-4" />
            New Project
          </Button>
        </div>

        {projects.length === 0 ? (
          <div className="p-8 text-center bg-white/50 rounded-lg border border-dashed border-slate-300 text-slate-500">
            No active projects found. Create one to get started!
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {topProjects.map((project: Project) => {
              const projectTasks = project.task || [];
              const totalTasks = projectTasks.length;
              const completedTasks = getCompletedCount(projectTasks);

              return (
                <ProjectSummaryCard
                  key={project.project_id}
                  id={String(project.project_id)}
                  name={project.project_name}
                  description={project.description}
                  completedTasks={completedTasks}
                  totalTasks={totalTasks}
                  color="#6366f1"
                />
              );
            })}
          </div>
        )}
      </div>

      {/* Today's Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <TaskOverview
            tasks={overviewTasks.map((t) => ({
              _id: String(t.task_id),
              title: t.task_name,
              status: t.status as "Pending" | "In Progress" | "Completed",
              description: t.description,
              dueDate: t.due_date,
              projectId: String(t.project_id),
            }))}
            isLoading={isLoading}
          />
        </div>
        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-6 text-white shadow-lg">
          <h3 className="font-bold text-lg mb-2">Pro Tip</h3>
          <p className="text-indigo-100 text-sm opacity-90">
            Breaking down complex tasks into smaller subtasks can increase productivity by 30%.
          </p>
        </div>
      </div>
    </div>
  );
}
