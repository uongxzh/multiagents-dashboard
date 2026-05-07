const statusConfig: Record<string, { color: string; label: string }> = {
  idle: { color: "bg-surface-500", label: "空闲" },
  working: { color: "bg-emerald-500", label: "工作中" },
  offline: { color: "bg-red-500", label: "离线" },
  online: { color: "bg-emerald-500", label: "在线" },
};

export default function AgentStatusBadge({ status }: { status: string }) {
  const cfg = statusConfig[status] || { color: "bg-surface-500", label: status };
  return (
    <div className="flex items-center gap-1.5">
      <span className={`h-2 w-2 rounded-full ${cfg.color}`} />
      <span className="text-xs text-surface-400">{cfg.label}</span>
    </div>
  );
}
