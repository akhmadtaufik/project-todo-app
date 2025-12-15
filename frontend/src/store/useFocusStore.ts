import { create } from 'zustand';

interface Task {
  _id: string;
  title: string;
  description?: string;
}

interface FocusState {
  isFocusMode: boolean;
  activeTask: Task | null;
  taskId: string | null;
  timer: number;
  initialTime: number;
  isRunning: boolean;
  projectId?: string;
  
  startFocus: (task: Task, projectId: string) => void;
  endFocus: () => void;
  toggleTimer: () => void;
  resetTimer: () => void;
  tick: () => void;
}

export const useFocusStore = create<FocusState>((set) => ({
  isFocusMode: false,
  activeTask: null,
  taskId: null,
  timer: 25 * 60, // 25 minutes in seconds
  initialTime: 25 * 60,
  isRunning: false,
  
  startFocus: (task, projectId) => set({ 
      isFocusMode: true, 
      activeTask: task, 
      taskId: task._id,
      projectId,
      timer: 25 * 60, 
      isRunning: true 
  }),
  
  endFocus: () => set({ 
      isFocusMode: false, 
      activeTask: null, 
      taskId: null,
      isRunning: false 
  }),
  
  toggleTimer: () => set((state) => ({ isRunning: !state.isRunning })),
  
  resetTimer: () => set((state) => ({ timer: state.initialTime, isRunning: false })),
  
  tick: () => set((state) => {
      if (state.timer > 0) {
          return { timer: state.timer - 1 };
      }
      return { isRunning: false };
  }),
}));
