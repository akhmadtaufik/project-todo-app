"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { KanbanBoard } from "@/components/dashboard/kanban/KanbanBoard";
import { Button } from "@/components/ui/button";
import { Settings, Plus } from "lucide-react";

interface Project {
  _id: string;
  name: string;
  description?: string;
}

interface Task {
  _id: string;
  title: string;
  description?: string;
  dueDate?: string;
  priority?: "Low" | "Medium" | "High";
  status: "Pending" | "In Progress" | "Completed";
  projectId: string;
}

// Mock Fetchers
const fetchProject = async (id: string): Promise<Project> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return { 
        _id: id, 
        name: id === "1" ? "Website Redesign" : "Mobile App Launch", 
        description: "Comprehensive overhaul of the main corporate website including new branding." 
    };
};

const fetchTasks = async (projectId: string): Promise<Task[]> => {
    await new Promise(resolve => setTimeout(resolve, 800));
    const today = new Date().toISOString().split('T')[0];
    
    if (projectId === "1") {
        return [
            { _id: "101", title: "Design System", description: "Create atomic components in Figma", status: "Completed", projectId, priority: "High", dueDate: today },
            { _id: "102", title: "Homepage Hero", description: "Implement new hero section with 3D elements", status: "In Progress", projectId, priority: "Medium" },
            { _id: "103", title: "Contact Form", description: "Zod validation schema and backend endpoint", status: "Pending", projectId, priority: "Low" },
            { _id: "104", title: "Footer Links", status: "Pending", projectId },
        ];
    }
    return [];
};

export default function ProjectPage() {
  const params = useParams();
  const id = params.id as string;

  const { data: project, isLoading: isLoadingProject } = useQuery({
    queryKey: ["project", id],
    queryFn: () => fetchProject(id),
  });

  const { data: tasks = [], isLoading: isLoadingTasks } = useQuery({
    queryKey: ["project-tasks", id],
    queryFn: () => fetchTasks(id),
  });

  if (isLoadingProject) {
      return <div className="animate-pulse space-y-4">
          <div className="h-8 w-64 bg-slate-200 rounded"></div>
          <div className="h-4 w-96 bg-slate-200 rounded"></div>
      </div>;
  }

  if (!project) return <div>Project not found</div>;

  return (
    <div className="flex flex-col h-full space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
            <h1 className="text-2xl font-bold text-slate-900">{project.name}</h1>
            <p className="text-slate-500 mt-1 max-w-2xl">{project.description}</p>
        </div>
        <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="gap-2">
                <Settings className="w-4 h-4" />
                Settings
            </Button>
            <Button size="sm" className="gap-2 bg-indigo-600 hover:bg-indigo-700">
                <Plus className="w-4 h-4" />
                New Task
            </Button>
        </div>
      </div>

      {/* Kanban Board */}
      <div className="flex-1 overflow-x-auto pb-4">
        {isLoadingTasks ? (
             <div className="grid grid-cols-3 gap-6">
                {[1,2,3].map(i => <div key={i} className="h-96 bg-slate-100 rounded-xl animate-pulse" />)}
             </div>
        ) : (
            <KanbanBoard initialTasks={tasks} projectId={id} />
        )}
      </div>
    </div>
  );
}
