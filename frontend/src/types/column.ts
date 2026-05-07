import type { Task } from "./task";

export interface Column {
  id: string;
  name: string;
  order: number;
  created_at: string | null;
  tasks: Task[];
}
