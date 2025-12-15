import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, Circle } from "lucide-react";
import { cn } from "@/lib/utils";

interface Task {
  _id: string;
  title: string;
  status: "Pending" | "In Progress" | "Completed";
  description?: string;
  dueDate?: string;
}

interface TaskOverviewProps {
  tasks: Task[];
  isLoading?: boolean;
}

export function TaskOverview({ tasks, isLoading }: TaskOverviewProps) {
  if (isLoading) {
    return <div>Loading tasks...</div>;
  }

  return (
    <Card className="border-0 shadow-none bg-transparent">
        <CardHeader className="px-0 pt-0">
            <CardTitle className="text-lg font-semibold text-slate-900">Today's Focus</CardTitle>
        </CardHeader>
        <CardContent className="px-0">
            {tasks.length === 0 ? (
                <div className="text-sm text-slate-500 italic">No tasks due today. Enjoy your day!</div>
            ) : (
                <div className="space-y-3">
                    {tasks.map(task => (
                        <div 
                            key={task._id} 
                            className="flex items-start gap-3 p-3 rounded-lg bg-white/70 border border-white/50 shadow-sm hover:shadow-md transition-all cursor-pointer group"
                        >
                            <button className="mt-0.5 text-slate-400 hover:text-indigo-600 transition-colors">
                                {task.status === "Completed" ? (
                                    <CheckCircle2 className="w-5 h-5 text-indigo-600" />
                                ) : (
                                    <Circle className="w-5 h-5" />
                                )}
                            </button>
                            <div className="flex-1">
                                <h4 className={cn(
                                    "text-sm font-medium text-slate-900 group-hover:text-indigo-700 transition-colors",
                                    task.status === "Completed" && "line-through text-slate-400"
                                )}>
                                    {task.title}
                                </h4>
                                {task.description && (
                                    <p className="text-xs text-slate-500 line-clamp-1 mt-0.5">{task.description}</p>
                                )}
                            </div>
                            <div className="text-xs font-medium text-slate-400 bg-slate-100 px-2 py-1 rounded">
                                {task.status}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </CardContent>
    </Card>
  );
}
