import type { Agent } from "./agent";

export type TaskStatus = "todo" | "in_progress" | "in_review" | "done";
export type TaskPriority = "low" | "medium" | "high" | "urgent";

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: TaskPriority;
  assignee_agent_id: string | null;
  creator_id: string | null;
  column_id: string | null;
  column_position: number;
  due_date: string | null;
  created_at: string | null;
  updated_at: string | null;
  assignee: Agent | null;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  assignee_agent_id?: string;
  column_id?: string;
  column_position?: number;
  due_date?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  assignee_agent_id?: string;
  column_id?: string;
  column_position?: number;
  due_date?: string;
}

export interface TaskMove {
  column_id: string;
  column_position?: number;
}
