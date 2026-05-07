import type { Agent } from "../../types/agent";
import AgentCard from "./AgentCard";

interface AgentGridProps {
  agents: Agent[];
  taskCounts?: Record<string, number>;
}

export default function AgentGrid({ agents, taskCounts }: AgentGridProps) {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {agents.map((agent) => (
        <AgentCard
          key={agent.id}
          agent={agent}
          taskCount={taskCounts?.[agent.id]}
        />
      ))}
    </div>
  );
}
