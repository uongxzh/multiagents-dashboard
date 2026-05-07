export default function LoadingSpinner({ text = "加载中..." }: { text?: string }) {
  return (
    <div className="flex items-center justify-center py-8">
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
      <span className="ml-3 text-surface-400">{text}</span>
    </div>
  );
}
