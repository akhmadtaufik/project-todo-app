/**
 * Project Service
 * 
 * Abstracts API calls for project operations.
 * Uses the configured axios instance from lib/axios.ts
 */
import api from '@/lib/axios';
import type { Project } from '@/types';

/**
 * Custom API Error class for standardized error handling
 */
export class ApiError extends Error {
  status: number;
  code?: string;

  constructor(message: string, status: number, code?: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

/**
 * Fetch parameters for getProjects
 */
export interface GetProjectsParams {
  page?: number;
  limit?: number;
}

/**
 * Fetch all projects with nested tasks
 * 
 * @param params - Optional pagination params
 * @returns Array of projects with tasks
 * @throws ApiError on failure
 */
export async function getProjects(params?: GetProjectsParams): Promise<Project[]> {
  try {
    const queryParams = new URLSearchParams();
    
    if (params?.page !== undefined) {
      queryParams.append('page', params.page.toString());
    }
    if (params?.limit !== undefined) {
      queryParams.append('limit', params.limit.toString());
    }

    const queryString = queryParams.toString();
    const url = queryString ? `/api/projects?${queryString}` : '/api/projects';
    
    const { data } = await api.get<Project[]>(url);
    
    // Ensure task array exists on each project
    return data.map((project: Project) => ({
      ...project,
      task: project.task || []
    }));
  } catch (error: unknown) {
    // Handle Axios errors
    if (error && typeof error === 'object' && 'response' in error) {
      const axiosError = error as { response?: { status: number; data?: { message?: string; error?: string } } };
      const status = axiosError.response?.status || 500;
      const message = axiosError.response?.data?.message 
        || axiosError.response?.data?.error 
        || 'Failed to fetch projects';
      
      throw new ApiError(message, status);
    }
    
    // Handle network errors
    if (error && typeof error === 'object' && 'request' in error) {
      throw new ApiError('Network error: Unable to reach server', 0, 'NETWORK_ERROR');
    }
    
    // Unknown error
    throw new ApiError('An unexpected error occurred', 500);
  }
}

/**
 * Get a single project by ID
 * 
 * @param projectId - Project ID
 * @returns Project with tasks
 * @throws ApiError on failure
 */
export async function getProjectById(projectId: number): Promise<Project> {
  try {
    const { data } = await api.get<Project>(`/api/projects/${projectId}`);
    return {
      ...data,
      task: data.task || []
    };
  } catch (error: unknown) {
    if (error && typeof error === 'object' && 'response' in error) {
      const axiosError = error as { response?: { status: number; data?: { message?: string; error?: string } } };
      const status = axiosError.response?.status || 500;
      const message = axiosError.response?.data?.message 
        || axiosError.response?.data?.error 
        || 'Failed to fetch project';
      
      throw new ApiError(message, status);
    }
    
    if (error && typeof error === 'object' && 'request' in error) {
      throw new ApiError('Network error: Unable to reach server', 0, 'NETWORK_ERROR');
    }
    
    throw new ApiError('An unexpected error occurred', 500);
  }
}
