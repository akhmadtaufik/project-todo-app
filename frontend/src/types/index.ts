/**
 * Shared TypeScript types matching backend Pydantic schemas
 */

// Task matching TaskResponse schema
export interface Task {
  task_id: number;
  task_name: string;
  description?: string;
  due_date?: string;
  status?: "Pending" | "In Progress" | "Completed";
  project_id: number;
  created_at?: string;
  update_at?: string;
}

// Project matching ProjectWithTasks schema (includes nested tasks)
export interface Project {
  project_id: number;
  project_name: string;
  description?: string;
  user_id: number;
  created_at?: string;
  update_at?: string;
  task: Task[];
}

// Basic project without tasks (for list views)
export interface ProjectBasic {
  project_id: number;
  project_name: string;
  description?: string;
  user_id: number;
  created_at?: string;
  update_at?: string;
}

// User type for auth context
export interface User {
  id: number;
  name: string;
  email: string;
}

// API Error structure
export interface ApiErrorResponse {
  message: string;
  status?: number;
  code?: string;
}
