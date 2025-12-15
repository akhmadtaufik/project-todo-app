"use client";

import { Droppable } from "@hello-pangea/dnd";
import { format, isSameMonth, isToday } from "date-fns";
import { cn } from "@/lib/utils";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Draggable } from "@hello-pangea/dnd"; // We might need Draggable here if we render tasks inside popover to be draggable
import { GripVertical } from "lucide-react";

interface Task {
  _id: string;
  title: string;
  status: string;
}

interface CalendarDayCellProps {
  date: Date;
  currentMonth: Date;
  tasks: Task[];
}

// Draggable Task Item inside Popover
function DraggableTaskItem({ task, index }: { task: Task; index: number }) {
    return (
        <Draggable draggableId={task._id} index={index}>
            {(provided) => (
                <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                    className="flex items-center gap-2 p-2 bg-white border border-slate-100 rounded-md mb-2 shadow-sm cursor-grab active:cursor-grabbing hover:bg-slate-50"
                >
                    <GripVertical className="w-4 h-4 text-slate-300" />
                    <span className="text-sm text-slate-700 truncate">{task.title}</span>
                    <span 
                        className={cn(
                            "ml-auto w-2 h-2 rounded-full",
                            task.status === "Completed" ? "bg-green-500" : "bg-amber-500"
                        )} 
                    />
                </div>
            )}
        </Draggable>
    );
}

export function CalendarDayCell({ date, currentMonth, tasks }: CalendarDayCellProps) {
  const isCurrentMonth = isSameMonth(date, currentMonth);
  const isDayToday = isToday(date);
  const dateStr = date.toISOString();

  return (
    <Droppable droppableId={dateStr} isDropDisabled={false}>
      {(provided, snapshot) => (
        <Popover>
            <PopoverTrigger asChild>
                <div
                ref={provided.innerRef}
                {...provided.droppableProps}
                className={cn(
                    "min-h-[100px] bg-white p-2 border-b border-r border-slate-100 transition-colors relative group hover:bg-slate-50 cursor-pointer",
                    !isCurrentMonth && "bg-slate-50/50 text-slate-400",
                    isDayToday && "bg-indigo-50/30",
                    snapshot.isDraggingOver && "bg-indigo-50 border-indigo-200 shadow-inner"
                )}
                >
                <div className="flex justify-between items-start">
                    <span 
                        className={cn(
                            "text-sm font-medium w-7 h-7 flex items-center justify-center rounded-full",
                            isDayToday && "bg-indigo-600 text-white"
                        )}
                    >
                        {format(date, "d")}
                    </span>
                    
                    {/* Simplified Indicators */}
                    {tasks.length > 0 && (
                        <div className="flex -space-x-1">
                            {tasks.slice(0, 3).map((task, i) => (
                                <div 
                                    key={i} 
                                    className={cn(
                                        "w-2 h-2 rounded-full ring-1 ring-white",
                                        task.status === "Completed" ? "bg-green-500" : "bg-amber-500"
                                    )} 
                                />
                            ))}
                            {tasks.length > 3 && (
                                <div className="w-2 h-2 rounded-full bg-slate-300 ring-1 ring-white" />
                            )}
                        </div>
                    )}
                </div>
                
                {/* Visual Placeholder for Dragging over empty days */}
                {provided.placeholder}
                </div>
            </PopoverTrigger>
            
            <PopoverContent className="w-72 p-0" align="start">
                <div className="p-3 bg-slate-50 border-b border-slate-100 font-medium text-slate-700 flex justify-between">
                    {format(date, "EEEE, MMMM d")}
                    <span className="text-xs text-slate-400 font-normal">{tasks.length} tasks</span>
                </div>
                <div className="p-2 max-h-64 overflow-y-auto">
                    {tasks.length === 0 ? (
                        <p className="text-sm text-slate-400 text-center py-4">No tasks due this day.</p>
                    ) : (
                        // Standard Div - Tasks inside here are draggable, BUT they need to be inside a Droppable context 
                        // which is usually the Grid itself or a specific list.
                        // However, Draggable must be child of Droppable. 
                        // If we want to move tasks FROM here, this PopoverContent represents the "Source" droppable ideally,
                        // OR we just cheat and say the day cell IS the droppable, and these are visual representations.
                        // BUT hello-pangea/dnd requires strict hierarchy.
                        // Since we have one big DnD context in the Grid, and we want to drag items TO other days,
                        // These items need to be draggable.
                        // We will render them as Draggable. But they need a parent Droppable.
                        // We can make the Popover content a Droppable zone for THIS day?
                        // Let's rely on the fact that if we use the same droppableId as the cell (dateStr), 
                        // it might work if the library handles the portal correctly.
                        
                        tasks.map((task, index) => (
                             <DraggableTaskItem key={task._id} task={task} index={index} />
                        ))
                    )}
                </div>
            </PopoverContent>
        </Popover>
      )}
    </Droppable>
  );
}
