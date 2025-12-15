"use client";

import { useEffect } from "react";
import { useFocusStore } from "@/store/useFocusStore";
import { Button } from "@/components/ui/button";
import { Play, Pause, X, CheckCircle, RotateCcw } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import confetti from "canvas-confetti";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

export function FocusOverlay() {
  const { 
      isFocusMode, 
      activeTask, 
      timer, 
      isRunning, 
      projectId,
      taskId,
      endFocus, 
      toggleTimer, 
      tick,
      resetTimer 
  } = useFocusStore();

  const queryClient = useQueryClient();

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRunning && isFocusMode) {
      interval = setInterval(() => {
        tick();
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning, isFocusMode, tick]);

  const updateStatus = useMutation({
    mutationFn: async () => {
         // Mock API call
         await new Promise(resolve => setTimeout(resolve, 800));
    },
    onMutate: () => {
        // Optimistic update would go here if we had access to the list state directly, 
        // but we are in an overlay. We'll rely on invalidation.
    },
    onSuccess: () => {
        toast.success("Task completed! Great job!");
        if (projectId) {
            queryClient.invalidateQueries({ queryKey: ["project-tasks", projectId] });
        }
    }
  });

  const handleComplete = async () => {
      // Trigger confetti
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });

      // Update task status
      if (taskId) {
         updateStatus.mutate();
      }

      // Close overlay after a brief delay to see confetti
      setTimeout(() => {
          endFocus();
      }, 2000);
  };

  if (!isFocusMode || !activeTask) return null;

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <AnimatePresence>
        {isFocusMode && (
            <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/98 backdrop-blur-sm text-white"
            >
                <Button 
                    variant="ghost" 
                    size="icon" 
                    className="absolute top-6 right-6 text-slate-400 hover:text-white"
                    onClick={endFocus}
                >
                    <X className="w-8 h-8" />
                </Button>

                <div className="flex flex-col items-center max-w-2xl w-full px-4 text-center space-y-12">
                    <div className="space-y-4">
                        <span className="text-indigo-400 font-medium tracking-widest uppercase text-sm">Focus Mode</span>
                        <h2 className="text-3xl md:text-5xl font-bold leading-tight">{activeTask.title}</h2>
                        {activeTask.description && (
                            <p className="text-slate-400 text-lg max-w-lg mx-auto">{activeTask.description}</p>
                        )}
                    </div>

                    <div className="font-mono text-8xl md:text-9xl font-bold tracking-tighter tabular-nums">
                        {formatTime(timer)}
                    </div>

                    <div className="flex items-center gap-6">
                        <Button 
                            variant="outline" 
                            size="icon"
                            className="w-16 h-16 rounded-full border-2 border-slate-700 bg-transparent text-slate-300 hover:bg-slate-800 hover:text-white hover:border-slate-500 transition-all"
                            onClick={toggleTimer}
                        >
                            {isRunning ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6 ml-1" />}
                        </Button>
                        
                        <Button 
                            size="lg"
                            className="h-16 px-8 rounded-full bg-indigo-600 hover:bg-indigo-500 text-lg font-semibold shadow-lg shadow-indigo-900/20 gap-3"
                            onClick={handleComplete}
                            disabled={updateStatus.isPending}
                        >
                            {updateStatus.isPending ? "Updating..." : (
                                <>
                                    <CheckCircle className="w-6 h-6" />
                                    Mark as Done
                                </>
                            )}
                        </Button>

                        <Button 
                            variant="ghost" 
                            size="icon"
                            className="w-16 h-16 rounded-full text-slate-500 hover:text-white hover:bg-slate-800 transition-all"
                            onClick={resetTimer}
                        >
                            <RotateCcw className="w-6 h-6" />
                        </Button>
                    </div>
                </div>
            </motion.div>
        )}
    </AnimatePresence>
  );
}
