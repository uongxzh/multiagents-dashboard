import { useState, useEffect, useCallback } from "react";
import { Plus } from "lucide-react";
import KanbanBoard from "../components/kanban/KanbanBoard";
import TaskForm from "../components/task/TaskForm";
import Modal from "../components/common/Modal";
import { createTask } from "../services/taskApi";
import { fetchAgents } from "../services/agentApi";
import { fetchColumns } from "../services/columnApi";
import type { TaskCreate } from "../types/task";
import type { Agent } from "../types/agent";

export default function KanbanPage() {
  const [showCreate, setShowCreate] = useState(false);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [columns, setColumns] = useState<{ id: string; name: string }[]>([]);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    fetchAgents().then(setAgents).catch(() => {});
    fetchColumns().then((cols) => setColumns(cols.map((c) => ({ id: c.id, name: c.name })))).catch(() => {});
  }, []);

  const handleCreate = useCallback(async (data: TaskCreate) => {
    try {
      await createTask(data);
      setShowCreate(false);
      setRefreshKey((k) => k + 1);
    } catch {
      alert("创建任务失败");
    }
  }, []);

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">任务看板</h1>
          <p className="mt-1 text-sm text-surface-400">拖拽任务卡片以改变状态</p>
        </div>
        <button
          onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500"
        >
          <Plus size={16} />
          新建任务
        </button>
      </div>

      <KanbanBoard key={refreshKey} />

      <Modal open={showCreate} onClose={() => setShowCreate(false)} title="新建任务">
        <TaskForm
          agents={agents}
          columns={columns}
          onSubmit={handleCreate}
          onCancel={() => setShowCreate(false)}
        />
      </Modal>
    </div>
  );
}
