"use client";

import { useQuery } from "@tanstack/react-query";
import { ProjectSummaryCard } from "@/components/dashboard/ProjectSummaryCard";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

interface Project {
  _id: string;
  name: string;
  description?: string;
  color?: string;
  updatedAt: string;
}

// Reuse logic/mock from dashboard page for now
const fetchProjects = async (): Promise<Project[]> => {
    await new Promise(resolve => setTimeout(resolve, 800));
    return [
        { _id: "1", name: "Website Redesign", description: "Revamping the corporate website", color: "#6366f1", updatedAt: "2023-12-01" },
        { _id: "2", name: "Mobile App Launch", description: "iOS and Android store submission", color: "#10b981", updatedAt: "2023-12-05" },
        { _id: "3", name: "Q4 Audit", description: "Financial audit preparation", color: "#f59e0b", updatedAt: "2023-11-20" },
        { _id: "4", name: "Internal Tools", description: "Updating employee dashboard", color: "#ec4899", updatedAt: "2023-10-15" },
        { _id: "5", name: "Marketing Campaign", description: "Q1 2024 Social Media Strategy", color: "#8b5cf6", updatedAt: "2023-12-10" },
    ];
};

export default function ProjectsPage() {
  const { data: projects = [], isLoading } = useQuery({
    queryKey: ["projects"],
    queryFn: fetchProjects,
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
            <h1 className="text-2xl font-bold text-slate-900">All Projects</h1>
            <p className="text-slate-500 mt-1">Manage your ongoing initiatives</p>
        </div>
        <Button className="bg-indigo-600 hover:bg-indigo-700 gap-2">
            <Plus className="w-4 h-4" />
            New Project
        </Button>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map(i => (
                <div key={i} className="h-48 bg-slate-200 rounded-xl animate-pulse" />
            ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
                <ProjectSummaryCard
                    key={project._id}
                    id={project._id}
                    name={project.name}
                    description={project.description}
                    completedTasks={3} // Mock data
                    totalTasks={8} // Mock data
                    color={project.color}
                />
            ))}
        </div>
      )}
    </div>
  );
}
