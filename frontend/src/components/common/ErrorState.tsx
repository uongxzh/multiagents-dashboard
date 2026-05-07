import { AlertTriangle, RefreshCw } from "lucide-react";

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export default function ErrorState({
  message = "加载失败",
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <AlertTriangle className="h-10 w-10 text-red-400" />
      <p className="mt-3 text-surface-400">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 flex items-center gap-2 rounded-lg bg-surface-800 px-4 py-2 text-sm text-white hover:bg-surface-700"
        >
          <RefreshCw size={16} />
          重试
        </button>
      )}
    </div>
  );
}
