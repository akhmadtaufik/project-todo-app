import { Droppable } from "@hello-pangea/dnd";
import { KanbanCard } from "./KanbanCard";
import { cn } from "@/lib/utils";

interface Task {
  _id: string;
  title: string;
  description?: string;
  dueDate?: string;
  priority?: "Low" | "Medium" | "High";
  status: "Pending" | "In Progress" | "Completed";
}

interface KanbanColumnProps {
  id: string;
  title: string;
  tasks: Task[];
  count: number;
}

export function KanbanColumn({ id, title, tasks, count }: KanbanColumnProps) {
  return (
    <div className="flex flex-col h-full bg-slate-100/50 rounded-xl p-4 border border-slate-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-slate-700">{title}</h3>
        <span className="text-xs font-medium text-slate-500 bg-slate-200 px-2 py-1 rounded-full">
            {count}
        </span>
      </div>

      <Droppable droppableId={id}>
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className={cn(
                "flex-1 transition-colors rounded-lg",
                snapshot.isDraggingOver && "bg-slate-200/50 border-2 border-dashed border-indigo-300"
            )}
          >
            {tasks.map((task, index) => (
              <KanbanCard key={task._id} task={task} index={index} />
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
  );
}
