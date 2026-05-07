import { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import { fetchTask } from "../services/taskApi";
import type { Task } from "../types/task";
import TaskDetailPanel from "../components/task/TaskDetailPanel";
import LoadingSpinner from "../components/common/LoadingSpinner";
import ErrorState from "../components/common/ErrorState";

export default function TaskDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTask(id);
      setTask(data);
    } catch {
      setError("加载任务失败");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { load(); }, [load]);

  if (loading) return <LoadingSpinner text="加载任务详情..." />;
  if (error) return <ErrorState message={error} onRetry={load} />;
  if (!task) return <ErrorState message="任务不存在" />;

  return <TaskDetailPanel task={task} />;
}
