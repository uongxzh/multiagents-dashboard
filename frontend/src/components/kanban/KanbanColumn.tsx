import { useDroppable } from "@dnd-kit/core";
import { SortableContext, verticalListSortingStrategy } from "@dnd-kit/sortable";
import type { Column } from "../../types/column";
import TaskCard from "./TaskCard";

interface KanbanColumnProps {
  column: Column;
}

export default function KanbanColumn({ column }: KanbanColumnProps) {
  const { setNodeRef, isOver } = useDroppable({ id: column.id });

  return (
    <div className="flex w-72 flex-shrink-0 flex-col rounded-xl bg-surface-900/60">
      <div className="mb-3 flex items-center justify-between px-4 pt-4">
        <h3 className="text-sm font-semibold text-white">{column.name}</h3>
        <span className="rounded-full bg-surface-800 px-2 py-0.5 text-xs text-surface-400">
          {column.tasks.length}
        </span>
      </div>
      <div
        ref={setNodeRef}
        className={`flex flex-1 flex-col gap-2 overflow-y-auto px-3 pb-3 transition-colors ${
          isOver ? "bg-surface-800/50" : ""
        }`}
        style={{ minHeight: 120 }}
      >
        <SortableContext items={column.tasks.map((t) => t.id)} strategy={verticalListSortingStrategy}>
          {column.tasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </SortableContext>
        {column.tasks.length === 0 && (
          <p className="py-6 text-center text-xs text-surface-500">拖拽任务到此</p>
        )}
      </div>
    </div>
  );
}
