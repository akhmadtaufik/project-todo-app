import { Draggable } from "@hello-pangea/dnd";
import { Card, CardContent } from "@/components/ui/card";
import { Calendar, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface Task {
  _id: string;
  title: string;
  description?: string;
  dueDate?: string;
  priority?: "Low" | "Medium" | "High";
}

interface KanbanCardProps {
  task: Task;
  index: number;
}

export function KanbanCard({ task, index }: KanbanCardProps) {
  return (
    <Draggable draggableId={task._id} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className="mb-3"
          style={{ ...provided.draggableProps.style }}
        >
          <Card 
            className={cn(
                "border-0 shadow-sm transition-all bg-white hover:shadow-md",
                snapshot.isDragging && "shadow-xl rotate-2 scale-105"
            )}
          >
            <CardContent className="p-4">
              <h4 className="font-medium text-slate-900 mb-1">{task.title}</h4>
              {task.description && (
                <p className="text-xs text-slate-500 line-clamp-2 mb-3">{task.description}</p>
              )}
              
              <div className="flex items-center justify-between mt-2">
                {task.dueDate && (
                     <div className={cn(
                        "flex items-center gap-1 text-xs px-2 py-1 rounded-full",
                        new Date(task.dueDate) < new Date() ? "bg-red-100 text-red-600" : "bg-slate-100 text-slate-600"
                     )}>
                        <Calendar className="w-3 h-3" />
                        <span>{new Date(task.dueDate).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}</span>
                     </div>
                )}
                
                {task.priority === "High" && (
                    <div className="flex items-center gap-1 text-xs text-amber-600 font-medium ml-auto">
                        <AlertCircle className="w-3 h-3" />
                        High
                    </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </Draggable>
  );
}
