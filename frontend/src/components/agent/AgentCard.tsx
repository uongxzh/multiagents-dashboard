import { Monitor, Tag } from "lucide-react";
import type { Agent } from "../../types/agent";
import AgentStatusBadge from "./AgentStatusBadge";

interface AgentCardProps {
  agent: Agent;
  taskCount?: number;
}

export default function AgentCard({ agent, taskCount }: AgentCardProps) {
  return (
    <div className="rounded-xl border border-surface-800 bg-surface-900 p-4 transition hover:border-surface-700 hover:bg-surface-800/80">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-800 text-xl">
            {agent.avatar || "🤖"}
          </span>
          <div>
            <h3 className="font-medium text-white">{agent.name}</h3>
            <div className="mt-0.5 flex items-center gap-1.5 text-xs text-surface-400">
              <Tag size={12} />
              <span>{agent.role}</span>
            </div>
          </div>
        </div>
        <AgentStatusBadge status={agent.status} />
      </div>
      <div className="mt-3 flex items-center justify-between text-xs text-surface-400">
        <div className="flex items-center gap-1">
          <Monitor size={12} />
          <span>{agent.environment}</span>
        </div>
        {taskCount !== undefined && <span>{taskCount} 个任务</span>}
      </div>
    </div>
  );
}
