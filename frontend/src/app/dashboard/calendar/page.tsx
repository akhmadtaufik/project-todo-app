"use client";

import { useQuery } from "@tanstack/react-query";
import { CalendarGrid } from "@/components/dashboard/calendar/CalendarGrid";
import { DashboardSkeleton } from "@/components/dashboard/DashboardSkeleton";

interface Task {
    _id: string;
    title: string;
    dueDate?: string;
    status: string;
}
  
const fetchAllTasks = async (): Promise<Task[]> => {
    // Mock API
    await new Promise(resolve => setTimeout(resolve, 800));
    const today = new Date().toISOString().split('T')[0];
    const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];
    const nextWeek = new Date(Date.now() + 86400000 * 7).toISOString().split('T')[0];
    
    return [
       { _id: "101", title: "Design System", status: "Completed", dueDate: today },
       { _id: "201", title: "App Store Assets", status: "Pending", dueDate: today },
       { _id: "102", title: "Homepage Hero", status: "In Progress", dueDate: tomorrow },
       { _id: "301", title: "Audit Report", status: "Pending", dueDate: nextWeek },
    ];
};

export default function CalendarPage() {
  const { data: tasks = [], isLoading } = useQuery({
    queryKey: ["all-tasks"],
    queryFn: fetchAllTasks,
  });

  if (isLoading) {
      return (
          <div className="space-y-4">
              <div className="h-8 w-48 bg-slate-200 rounded animate-pulse" />
              <div className="h-[600px] bg-slate-100 rounded-xl animate-pulse" />
          </div>
      );
  }

  return (
    <div className="space-y-6">
        <div>
            <h1 className="text-2xl font-bold text-slate-900">Calendar</h1>
            <p className="text-slate-500 mt-1">Timeline view of all project tasks</p>
        </div>
        
        <CalendarGrid tasks={tasks} />
    </div>
  );
}
