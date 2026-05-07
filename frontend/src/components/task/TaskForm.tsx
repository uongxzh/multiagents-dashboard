import { useState, type FormEvent } from "react";
import type { Agent } from "../../types/agent";
import type { TaskCreate, TaskPriority, TaskStatus } from "../../types/task";

interface TaskFormProps {
  agents: Agent[];
  columns: { id: string; name: string }[];
  onSubmit: (data: TaskCreate) => void;
  onCancel: () => void;
}

export default function TaskForm({ agents, columns, onSubmit, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<TaskPriority>("medium");
  const [assigneeId, setAssigneeId] = useState("");
  const [columnId, setColumnId] = useState(columns[0]?.id || "");
  const [dueDate, setDueDate] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    onSubmit({
      title: title.trim(),
      description: description.trim() || undefined,
      priority,
      assignee_agent_id: assigneeId || undefined,
      column_id: columnId || undefined,
      due_date: dueDate ? new Date(dueDate).toISOString() : undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="mb-1 block text-sm text-surface-300">标题 *</label>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full rounded-lg border border-surface-700 bg-surface-800 px-3 py-2 text-white placeholder-surface-500 outline-none focus:border-indigo-500"
          placeholder="输入任务标题"
          required
        />
      </div>
      <div>
        <label className="mb-1 block text-sm text-surface-300">描述</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full rounded-lg border border-surface-700 bg-surface-800 px-3 py-2 text-white placeholder-surface-500 outline-none focus:border-indigo-500"
          placeholder="可选描述"
        />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="mb-1 block text-sm text-surface-300">优先级</label>
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value as TaskPriority)}
            className="w-full rounded-lg border border-surface-700 bg-surface-800 px-3 py-2 text-white outline-none focus:border-indigo-500"
          >
            <option value="low">低</option>
            <option value="medium">中</option>
            <option value="high">高</option>
            <option value="urgent">紧急</option>
          </select>
        </div>
        <div>
          <label className="mb-1 block text-sm text-surface-300">看板列</label>
          <select
            value={columnId}
            onChange={(e) => setColumnId(e.target.value)}
            className="w-full rounded-lg border border-surface-700 bg-surface-800 px-3 py-2 text-white outline-none focus:border-indigo-500"
          >
            {columns.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="mb-1 block text-sm text-surface-300">指派给</label>
          <select
            value={assigneeId}
            onChange={(e) => setAssigneeId(e.target.value)}
            className="w-full rounded-lg border border-surface-700 bg-surface-800 px-3 py-2 text-white outline-none focus:border-indigo-500"
          >
            <option value="">未指派</option>
            {agents.map((a) => (
              <option key={a.id} value={a.id}>{a.avatar} {a.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="mb-1 block text-sm text-surface-300">截止日期</label>
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="w-full rounded-lg border border-surface-700 bg-surface-800 px-3 py-2 text-white outline-none focus:border-indigo-500"
          />
        </div>
      </div>
      <div className="flex justify-end gap-3 pt-2">
        <button type="button" onClick={onCancel} className="rounded-lg px-4 py-2 text-sm text-surface-300 hover:bg-surface-800">
          取消
        </button>
        <button type="submit" className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500">
          创建
        </button>
      </div>
    </form>
  );
}
