import { useState, useEffect, useCallback } from "react";
import {
  DndContext,
  DragOverlay,
  closestCorners,
  PointerSensor,
  useSensor,
  useSensors,
  type DragStartEvent,
  type DragEndEvent,
} from "@dnd-kit/core";
import type { Column } from "../../types/column";
import type { Task } from "../../types/task";
import { fetchColumns } from "../../services/columnApi";
import { moveTask } from "../../services/taskApi";
import KanbanColumn from "./KanbanColumn";
import TaskCard from "./TaskCard";
import LoadingSpinner from "../common/LoadingSpinner";
import ErrorState from "../common/ErrorState";

export default function KanbanBoard() {
  const [columns, setColumns] = useState<Column[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTask, setActiveTask] = useState<Task | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchColumns();
      setColumns(data);
    } catch {
      setError("加载看板失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } })
  );

  const handleDragStart = (event: DragStartEvent) => {
    const task = event.active.data.current?.task as Task | undefined;
    if (task) setActiveTask(task);
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    setActiveTask(null);
    const { active, over } = event;
    if (!over) return;

    const taskId = active.id as string;
    const overId = over.id as string;

    // Find which column the task belongs to, and which column was dropped on
    let fromColumn: Column | undefined;
    let task: Task | undefined;
    for (const col of columns) {
      const found = col.tasks.find((t) => t.id === taskId);
      if (found) { fromColumn = col; task = found; break; }
    }
    // Drop target could be a column or a task
    let toColumn: Column | undefined;
    for (const col of columns) {
      if (col.id === overId) { toColumn = col; break; }
      if (col.tasks.find((t) => t.id === overId)) { toColumn = col; break; }
    }
    if (!task || !toColumn || fromColumn?.id === toColumn.id) return;

    // Optimistic update
    setColumns((prev) =>
      prev.map((col) => ({
        ...col,
        tasks: col.id === fromColumn?.id
          ? col.tasks.filter((t) => t.id !== taskId)
          : col.id === toColumn.id
            ? [...col.tasks, { ...task, column_id: toColumn.id, column_position: col.tasks.length + 1 }]
            : col.tasks,
      }))
    );

    try {
      await moveTask(taskId, { column_id: toColumn.id, column_position: toColumn.tasks.length + 1 });
      await load(); // Reload for accurate positions
    } catch {
      await load(); // Revert on error
    }
  };

  if (loading) return <LoadingSpinner text="加载看板..." />;
  if (error) return <ErrorState message={error} onRetry={load} />;

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCorners}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <div className="flex gap-4 overflow-x-auto pb-4">
        {columns.map((col) => (
          <KanbanColumn key={col.id} column={col} />
        ))}
      </div>
      <DragOverlay>
        {activeTask ? <div className="w-72"><TaskCard task={activeTask} /></div> : null}
      </DragOverlay>
    </DndContext>
  );
}
