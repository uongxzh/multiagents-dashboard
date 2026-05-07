import { Calendar, User, Clock, ArrowLeft } from "lucide-react";
import type { Task } from "../../types/task";
import PriorityBadge from "./PriorityBadge";
import { useNavigate } from "react-router-dom";

interface TaskDetailPanelProps {
  task: Task;
}

const statusLabels: Record<string, string> = {
  todo: "待办",
  in_progress: "进行中",
  in_review: "审核中",
  done: "已完成",
};

export default function TaskDetailPanel({ task }: TaskDetailPanelProps) {
  const navigate = useNavigate();

  return (
    <div className="mx-auto max-w-2xl">
      <button
        onClick={() => navigate("/kanban")}
        className="mb-6 flex items-center gap-1 text-sm text-surface-400 hover:text-white"
      >
        <ArrowLeft size={16} />
        返回看板
      </button>

      <div className="rounded-xl border border-surface-800 bg-surface-900 p-6">
        <div className="mb-4 flex items-start justify-between">
          <h1 className="text-xl font-bold text-white">{task.title}</h1>
          <PriorityBadge priority={task.priority} />
        </div>

        <div className="mb-6 flex flex-wrap gap-4 text-sm">
          <div className="flex items-center gap-1.5 text-surface-400">
            <Clock size={14} />
            <span>{statusLabels[task.status] || task.status}</span>
          </div>
          {task.assignee && (
            <div className="flex items-center gap-1.5 text-surface-400">
              <User size={14} />
              <span>{task.assignee.avatar} {task.assignee.name}</span>
            </div>
          )}
          {task.due_date && (
            <div className="flex items-center gap-1.5 text-surface-400">
              <Calendar size={14} />
              <span>{new Date(task.due_date).toLocaleDateString("zh-CN")}</span>
            </div>
          )}
        </div>

        {task.description && (
          <div className="border-t border-surface-800 pt-4">
            <h3 className="mb-2 text-sm font-medium text-surface-300">描述</h3>
            <p className="whitespace-pre-wrap text-sm text-surface-400">{task.description}</p>
          </div>
        )}

        <div className="mt-4 border-t border-surface-800 pt-4 text-xs text-surface-500">
          <p>创建时间: {task.created_at ? new Date(task.created_at).toLocaleString("zh-CN") : "未知"}</p>
          {task.updated_at && <p>更新时间: {new Date(task.updated_at).toLocaleString("zh-CN")}</p>}
        </div>
      </div>
    </div>
  );
}
