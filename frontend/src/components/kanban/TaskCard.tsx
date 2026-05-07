import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { Calendar, User, GripVertical } from "lucide-react";
import type { Task } from "../../types/task";
import PriorityBadge from "../task/PriorityBadge";
import { useNavigate } from "react-router-dom";

interface TaskCardProps {
  task: Task;
}

export default function TaskCard({ task }: TaskCardProps) {
  const navigate = useNavigate();
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: task.id,
    data: { type: "task", task },
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  const dueDate = task.due_date ? new Date(task.due_date).toLocaleDateString("zh-CN") : null;

  return (
    <div
      ref={setNodeRef}
      style={style}
      className="group rounded-lg border border-surface-700 bg-surface-800 p-3 hover:border-surface-600 cursor-pointer"
      onClick={() => navigate(`/tasks/${task.id}`)}
    >
      <div className="flex items-start gap-2">
        <button
          {...attributes}
          {...listeners}
          className="mt-0.5 flex-shrink-0 cursor-grab text-surface-500 opacity-0 transition group-hover:opacity-100"
          onClick={(e) => e.stopPropagation()}
        >
          <GripVertical size={14} />
        </button>
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <h4 className="truncate text-sm font-medium text-white">{task.title}</h4>
          </div>
          <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-surface-400">
            <PriorityBadge priority={task.priority} />
            <span className="rounded bg-surface-700 px-1.5 py-0.5 text-surface-300">
              {task.status === "todo" ? "待办" : task.status === "in_progress" ? "进行中" : task.status === "in_review" ? "审核中" : "已完成"}
            </span>
          </div>
          <div className="mt-2 flex items-center gap-3 text-xs text-surface-500">
            {task.assignee && (
              <span className="flex items-center gap-1">
                <User size={12} />
                {task.assignee.avatar} {task.assignee.name}
              </span>
            )}
            {dueDate && (
              <span className="flex items-center gap-1">
                <Calendar size={12} />
                {dueDate}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
