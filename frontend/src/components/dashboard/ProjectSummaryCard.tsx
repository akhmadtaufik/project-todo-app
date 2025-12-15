import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ProjectSummaryCardProps {
  id: string;
  name: string;
  description?: string;
  completedTasks: number;
  totalTasks: number;
  color?: string;
}

export function ProjectSummaryCard({
  id,
  name,
  description,
  completedTasks,
  totalTasks,
  color = "#6366f1",
}: ProjectSummaryCardProps) {
  const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  return (
    <Link href={`/dashboard/projects/${id}`} className="block group">
      <Card className="h-full hover:shadow-md transition-shadow duration-200 border-white/40 bg-white/60 backdrop-blur-sm">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-base font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors">
            {name}
          </CardTitle>
          <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400">
             <MoreHorizontal className="h-4 w-4" />
          </Button>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-slate-500 line-clamp-2 mb-4 h-10">
            {description || "No description provided."}
          </p>
          
          <div className="space-y-2">
             <div className="flex items-center justify-between text-xs font-medium text-slate-600">
                <span>Progress</span>
                <span>{Math.round(progress)}%</span>
             </div>
             {/* Simple Custom Progress Bar */}
             <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                <div 
                    className="h-full rounded-full transition-all duration-500 ease-out"
                    style={{ 
                        width: `${progress}%`,
                        backgroundColor: color
                    }}
                />
             </div>
             <div className="flex items-center justify-between text-xs text-slate-400 mt-1">
                <span>{completedTasks} / {totalTasks} Tasks</span>
             </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
