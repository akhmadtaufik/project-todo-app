"use client";

import { useState, useEffect } from "react";
import { DragDropContext, DropResult } from "@hello-pangea/dnd";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { KanbanColumn } from "./KanbanColumn";
import { toast } from "sonner";
import axios from "axios";

interface Task {
  _id: string;
  title: string;
  description?: string;
  dueDate?: string;
  priority?: "Low" | "Medium" | "High";
  status: "Pending" | "In Progress" | "Completed";
  projectId: string;
}

interface KanbanBoardProps {
  initialTasks: Task[];
  projectId: string;
}

export function KanbanBoard({ initialTasks, projectId }: KanbanBoardProps) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const queryClient = useQueryClient();

  useEffect(() => {
    setTasks(initialTasks);
  }, [initialTasks]);

  const updateTaskStatus = useMutation({
    mutationFn: async ({ taskId, status }: { taskId: string; status: string }) => {
      // Mock API call
      // await axios.put(`/api/project/${projectId}/task/${taskId}`, { status });
      await new Promise(resolve => setTimeout(resolve, 500)); 
    },
    onMutate: async ({ taskId, status }) => {
        // Optimistic Update
        const previousTasks = tasks;
        
        setTasks((prev) => 
            prev.map(t => t._id === taskId ? { ...t, status: status as any } : t)
        );

        return { previousTasks };
    },
    onError: (err, newTodo, context) => {
        // Rollback
        if (context?.previousTasks) {
            setTasks(context.previousTasks);
        }
        toast.error("Failed to update task status");
    },
    onSettled: () => {
        // Invalidate to fetch fresh data
         queryClient.invalidateQueries({ queryKey: ["project-tasks", projectId] });
    }
  });

  const onDragEnd = (result: DropResult) => {
    const { destination, source, draggableId } = result;

    if (!destination) return;

    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    const newStatus = destination.droppableId;
    
    // UI Update immediately handled by local state in onMutate, 
    // but we trigger mutation here
    updateTaskStatus.mutate({ taskId: draggableId, status: newStatus });
  };

  const columns = [
    { id: "Pending", title: "To Do" },
    { id: "In Progress", title: "In Progress" },
    { id: "Completed", title: "Done" },
  ];

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-full min-h-[500px]">
        {columns.map((col) => {
            const columnTasks = tasks.filter(task => task.status === col.id);
            return (
                <KanbanColumn 
                    key={col.id} 
                    id={col.id} 
                    title={col.title} 
                    tasks={columnTasks}
                    count={columnTasks.length}
                />
            );
        })}
      </div>
    </DragDropContext>
  );
}
