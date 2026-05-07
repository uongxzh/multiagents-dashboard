import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import { LayoutDashboard, Columns3 } from "lucide-react";
import DashboardPage from "./pages/DashboardPage";
import KanbanPage from "./pages/KanbanPage";
import TaskDetailPage from "./pages/TaskDetailPage";

function Sidebar() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition ${
      isActive
        ? "bg-indigo-600/20 text-indigo-400"
        : "text-surface-400 hover:bg-surface-800 hover:text-white"
    }`;

  return (
    <aside className="flex w-56 flex-col border-r border-surface-800 bg-surface-950 p-4">
      <div className="mb-8 flex items-center gap-2 px-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-sm font-bold text-white">
          ZX
        </div>
        <span className="font-semibold text-white">Agent Dashboard</span>
      </div>
      <nav className="flex flex-col gap-1">
        <NavLink to="/" end className={linkClass}>
          <LayoutDashboard size={18} />
          仪表盘
        </NavLink>
        <NavLink to="/kanban" className={linkClass}>
          <Columns3 size={18} />
          任务看板
        </NavLink>
      </nav>
    </aside>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-surface-950">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/kanban" element={<KanbanPage />} />
            <Route path="/tasks/:id" element={<TaskDetailPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
