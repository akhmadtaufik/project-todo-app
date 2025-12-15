"use client";

import { useState } from "react";
import { 
    startOfMonth, endOfMonth, startOfWeek, endOfWeek, 
    eachDayOfInterval, format, addMonths, subMonths, isSameMonth
} from "date-fns";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { CalendarDayCell } from "./CalendarDayCell";
import { DragDropContext, DropResult } from "@hello-pangea/dnd";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

interface Task {
  _id: string;
  title: string;
  dueDate?: string;
  status: string;
}

interface CalendarGridProps {
  tasks: Task[];
}

export function CalendarGrid({ tasks }: CalendarGridProps) {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const queryClient = useQueryClient();

  const handlePrevMonth = () => setCurrentMonth(subMonths(currentMonth, 1));
  const handleNextMonth = () => setCurrentMonth(addMonths(currentMonth, 1));

  // Generate grid dates
  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(monthStart);
  const startDate = startOfWeek(monthStart);
  const endDate = endOfWeek(monthEnd);

  const calendarDays = eachDayOfInterval({ start: startDate, end: endDate });

  const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  // Mutation for rescheduling
  const updateTaskDate = useMutation({
      mutationFn: async ({ taskId, date }: { taskId: string; date: string }) => {
          // Mock API call
          await new Promise(resolve => setTimeout(resolve, 500));
      },
      onMutate: async ({ taskId, date }) => {
          await queryClient.cancelQueries({ queryKey: ["all-tasks"] });
          const previousTasks = queryClient.getQueryData<Task[]>(["all-tasks"]);
          
          if (previousTasks) {
               queryClient.setQueryData<Task[]>(["all-tasks"], (old) => 
                  old?.map(t => t._id === taskId ? { ...t, dueDate: date } : t) || []
               );
          }
          return { previousTasks };
      },
      onError: (err, newTodo, context) => {
          if (context?.previousTasks) {
               queryClient.setQueryData(["all-tasks"], context.previousTasks);
          }
          toast.error("Failed to reschedule task");
      },
      onSettled: () => {
          queryClient.invalidateQueries({ queryKey: ["all-tasks"] });
          toast.success("Task rescheduled!");
      }
  });

  const onDragEnd = (result: DropResult) => {
      const { destination, draggableId } = result;
      if (!destination) return;
      
      const newDateStr = destination.droppableId; // We used dateStr as droppableId
      
      // Update logic
      updateTaskDate.mutate({ taskId: draggableId, date: newDateStr });
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-900">
           {format(currentMonth, "MMMM yyyy")}
        </h2>
        <div className="flex items-center gap-2">
            <Button variant="outline" size="icon" onClick={handlePrevMonth}>
                <ChevronLeft className="w-4 h-4" />
            </Button>
            <Button variant="outline" size="icon" onClick={handleNextMonth}>
                <ChevronRight className="w-4 h-4" />
            </Button>
        </div>
      </div>

      <DragDropContext onDragEnd={onDragEnd}>
        <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
            {/* Week Headers */}
            <div className="grid grid-cols-7 border-b border-slate-200 bg-slate-50">
                {weekDays.map(day => (
                    <div key={day} className="py-2 text-center text-xs font-semibold text-slate-500 uppercase tracking-wide">
                        {day}
                    </div>
                ))}
            </div>

            {/* Days Grid */}
            <div className="grid grid-cols-7 auto-rows-fr">
                {calendarDays.map((day, idx) => {
                    const dateStr = format(day, "yyyy-MM-dd");
                    const dayTasks = tasks.filter(t => {
                        if (!t.dueDate) return false;
                        return t.dueDate.startsWith(dateStr);
                    });

                    return (
                        <CalendarDayCell 
                            key={day.toString()} 
                            date={day} 
                            currentMonth={currentMonth}
                            tasks={dayTasks}
                        />
                    );
                })}
            </div>
        </div>
      </DragDropContext>
    </div>
  );
}
