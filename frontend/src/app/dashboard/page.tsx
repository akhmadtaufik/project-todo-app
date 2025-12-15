"use client";

import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { DashboardSkeleton } from "@/components/dashboard/DashboardSkeleton";
import { GreetingSection } from "@/components/dashboard/GreetingSection";
import { ProjectSummaryCard } from "@/components/dashboard/ProjectSummaryCard";
import { TaskOverview } from "@/components/dashboard/TaskOverview";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

interface Project {
  _id: string;
  name: string;
  description?: string;
  color?: string;
  updatedAt: string;
}

interface Task {
  _id: string;
  title: string;
  status: "Pending" | "In Progress" | "Completed";
  description?: string;
  dueDate?: string;
  projectId: string;
}

// Mock Data Function (Replace with actual API)
const fetchProjects = async (): Promise<Project[]> => {
    // try {
    //     const { data } = await axios.get("/api/projects");
    //     return data;
    // } catch (e) {
        // Return mock if API fails
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate latency
        return [
            { _id: "1", name: "Website Redesign", description: "Revamping the corporate website", color: "#6366f1", updatedAt: "2023-12-01" },
            { _id: "2", name: "Mobile App Launch", description: "iOS and Android store submission", color: "#10b981", updatedAt: "2023-12-05" },
            { _id: "3", name: "Q4 Audit", description: "Financial audit preparation", color: "#f59e0b", updatedAt: "2023-11-20" },
            { _id: "4", name: "Internal Tools", description: "Updating employee dashboard", color: "#ec4899", updatedAt: "2023-10-15" },
        ];
    // }
};

const fetchProjectTasks = async (projectId: string): Promise<Task[]> => {
    // Mock tasks based on project ID
    await new Promise(resolve => setTimeout(resolve, 500));
    const today = new Date().toISOString().split('T')[0];
    
    const mockTasks: Record<string, Task[]> = {
        "1": [
            { _id: "101", title: "Design System", status: "Completed", projectId: "1", dueDate: today },
            { _id: "102", title: "Homepage Hero", status: "In Progress", projectId: "1", dueDate: today },
            { _id: "103", title: "Contact Form", status: "Pending", projectId: "1" },
        ],
        "2": [
            { _id: "201", title: "App Store Assets", status: "Pending", projectId: "2", dueDate: today },
        ],
        "3": [],
    };
    return mockTasks[projectId] || [];
};

export default function DashboardPage() {
  const { data: projects = [], isLoading: isLoadingProjects } = useQuery({
    queryKey: ["projects"],
    queryFn: fetchProjects,
  });

  // Fetch tasks for top 3 projects to calculate progress/show today's tasks
  // In a real app, we might want a dedicated 'dashboard-stats' endpoint to avoid waterfall or over-fetching
  const topProjects = projects.slice(0, 3);
  
  const { data: tasksResults = [], isLoading: isLoadingTasks } = useQuery({
    queryKey: ["dashboard-tasks", topProjects.map(p => p._id).join(',')],
    queryFn: async () => {
        if (topProjects.length === 0) return [];
        const promises = topProjects.map(p => fetchProjectTasks(p._id));
        const results = await Promise.all(promises);
        return results.flat();
    },
    enabled: topProjects.length > 0,
  });

  const isLoading = isLoadingProjects || (projects.length > 0 && isLoadingTasks);

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  // Calculate Aggregates
  const tasksDueToday = tasksResults.filter(t => {
      if (!t.dueDate) return false;
      const today = new Date().toISOString().split('T')[0];
      return t.dueDate.startsWith(today) && t.status !== "Completed";
  });
  
  const pendingTasksCount = tasksDueToday.length;

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <GreetingSection 
        userName="User" // TODO: Get from auth context
        pendingTasksCount={pendingTasksCount}
      />

      {/* Projects Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-slate-900">Active Projects</h2>
            <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700 text-white gap-2 shadow-indigo-200 shadow-md">
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
            {topProjects.map((project) => {
                // Calculate progress from fetched tasks for this project
                const projectTasks = tasksResults.filter(t => t.projectId === project._id);
                const total = projectTasks.length || 5; // Mock total if 0 to show some UI
                const completed = projectTasks.filter(t => t.status === "Completed").length || (project._id === "1" ? 1 : 0);
                
                return (
                    <ProjectSummaryCard
                        key={project._id}
                        id={project._id}
                        name={project._id === "2" ? "Mobile App Launch" : project.name} // Just ensuring name match
                        description={project.description}
                        completedTasks={completed}
                        totalTasks={total}
                        color={project.color}
                    />
                );
            })}
            </div>
        )}
      </div>

      {/* Today's Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
            <TaskOverview tasks={tasksDueToday.concat(tasksResults.filter(t => t.status === "In Progress" && !tasksDueToday.includes(t)))} isLoading={isLoading} />
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
