import { Draggable } from "@hello-pangea/dnd";
import { Card, CardContent } from "@/components/ui/card";
import { Calendar, AlertCircle, Play } from "lucide-react"; // Import Play
import { cn } from "@/lib/utils";
import { useFocusStore } from "@/store/useFocusStore"; // Import store
import { Button } from "@/components/ui/button";

interface Task {
  _id: string;
  title: string;
  description?: string;
  dueDate?: string;
  priority?: "Low" | "Medium" | "High";
  projectId?: string;
}

interface KanbanCardProps {
  task: Task;
  index: number;
}

export function KanbanCard({ task, index }: KanbanCardProps) {
  const { startFocus } = useFocusStore();

  const handleStartFocus = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent drag interference if possible, though dnd handle is usually separate or wrapper
    // Assuming projectId is passed or we extract it. For now using placeholder or prop if available.
    // In strict Implementation, KanbanCard might need projectId prop. 
    // We'll use task.projectId if available, else a placeholder.
    startFocus(task, task.projectId || "unknown");
  };

  return (
    <Draggable draggableId={task._id} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className="mb-3 group relative" // Added relative group
          style={{ ...provided.draggableProps.style }}
        >
          <Card 
            className={cn(
                "border-0 shadow-sm transition-all bg-white hover:shadow-md",
                snapshot.isDragging && "shadow-xl rotate-2 scale-105"
            )}
          >
            <CardContent className="p-4">
              <div className="flex justify-between items-start gap-2">
                 <h4 className="font-medium text-slate-900 mb-1">{task.title}</h4>
                 {/* Focus Trigger - Visible on hover */}
                 <Button 
                    variant="ghost" 
                    size="icon" 
                    className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50"
                    onClick={handleStartFocus}
                    title="Start Focus Mode"
                 >
                    <Play className="w-3 h-3 fill-current" />
                 </Button>
              </div>

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
