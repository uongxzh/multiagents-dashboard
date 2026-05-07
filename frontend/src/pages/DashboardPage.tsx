import { useEffect, useState, useCallback } from "react";
import { fetchAgents } from "../services/agentApi";
import { fetchTasks } from "../services/taskApi";
import type { Agent } from "../types/agent";
import type { Task } from "../types/task";
import AgentGrid from "../components/agent/AgentGrid";
import { Users, ListTodo, Clock, CheckCircle2 } from "lucide-react";
import LoadingSpinner from "../components/common/LoadingSpinner";
import ErrorState from "../components/common/ErrorState";

export default function DashboardPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [agentsData, tasksData] = await Promise.all([fetchAgents(), fetchTasks()]);
      setAgents(agentsData);
      setTasks(tasksData);
    } catch {
      setError("加载数据失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  if (loading) return <LoadingSpinner text="加载仪表盘..." />;
  if (error) return <ErrorState message={error} onRetry={load} />;

  const stats = [
    { icon: Users, label: "Agent 总数", value: agents.length, color: "text-indigo-400" },
    { icon: ListTodo, label: "任务总数", value: tasks.length, color: "text-blue-400" },
    { icon: Clock, label: "进行中", value: tasks.filter((t) => t.status === "in_progress").length, color: "text-yellow-400" },
    { icon: CheckCircle2, label: "已完成", value: tasks.filter((t) => t.status === "done").length, color: "text-emerald-400" },
  ];

  // Count tasks per agent
  const taskCounts: Record<string, number> = {};
  for (const t of tasks) {
    if (t.assignee_agent_id) {
      taskCounts[t.assignee_agent_id] = (taskCounts[t.assignee_agent_id] || 0) + 1;
    }
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Agent Cluster Dashboard</h1>
        <p className="mt-1 text-sm text-surface-400">zx007 Agent 集群状态与任务总览</p>
      </div>

      {/* Stats cards */}
      <div className="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
        {stats.map((stat) => (
          <div key={stat.label} className="rounded-xl border border-surface-800 bg-surface-900 p-4">
            <div className="flex items-center gap-3">
              <stat.icon className={`h-8 w-8 ${stat.color}`} />
              <div>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
                <p className="text-xs text-surface-400">{stat.label}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Agent grid */}
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">Agent 列表</h2>
        <span className="text-sm text-surface-400">
          {agents.filter((a) => a.status === "working").length} 个工作 &middot;{" "}
          {agents.filter((a) => a.status === "idle").length} 个空闲
        </span>
      </div>
      <AgentGrid agents={agents} taskCounts={taskCounts} />
    </div>
  );
}
