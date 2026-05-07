import { ChevronUp } from "lucide-react";
import type { TaskPriority } from "../../types/task";

const config: Record<TaskPriority, { color: string; label: string }> = {
  low: { color: "text-surface-400", label: "低" },
  medium: { color: "text-yellow-400", label: "中" },
  high: { color: "text-orange-400", label: "高" },
  urgent: { color: "text-red-400", label: "紧急" },
};

export default function PriorityBadge({ priority }: { priority: TaskPriority }) {
  const cfg = config[priority] || config.medium;
  return (
    <span className={`flex items-center gap-0.5 text-xs font-medium ${cfg.color}`}>
      <ChevronUp size={12} />
      {cfg.label}
    </span>
  );
}
