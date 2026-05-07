import api from "./api";
import type { Task, TaskCreate, TaskUpdate, TaskMove } from "../types/task";

export async function fetchTasks(params?: {
  status?: string;
  priority?: string;
  assignee?: string;
}): Promise<Task[]> {
  const res = await api.get("/tasks", { params });
  return res.data;
}

export async function fetchTask(id: string): Promise<Task> {
  const res = await api.get(`/tasks/${id}`);
  return res.data;
}

export async function createTask(data: TaskCreate): Promise<Task> {
  const res = await api.post("/tasks", data);
  return res.data;
}

export async function updateTask(id: string, data: TaskUpdate): Promise<Task> {
  const res = await api.put(`/tasks/${id}`, data);
  return res.data;
}

export async function deleteTask(id: string): Promise<void> {
  await api.delete(`/tasks/${id}`);
}

export async function moveTask(id: string, data: TaskMove): Promise<Task> {
  const res = await api.patch(`/tasks/${id}/move`, data);
  return res.data;
}
