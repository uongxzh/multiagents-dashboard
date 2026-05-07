interface BadgeProps {
  children: string;
}

const colorMap: Record<string, string> = {
  low: "bg-surface-600 text-surface-200",
  medium: "bg-yellow-900/60 text-yellow-300",
  high: "bg-orange-900/60 text-orange-300",
  urgent: "bg-red-900/60 text-red-300",
  idle: "bg-surface-600 text-surface-200",
  working: "bg-emerald-900/60 text-emerald-300",
  offline: "bg-red-900/60 text-red-300",
  online: "bg-emerald-900/60 text-emerald-300",
};

export default function Badge({ children }: BadgeProps) {
  const cls = colorMap[children] || "bg-surface-600 text-surface-200";
  return (
    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${cls}`}>
      {children}
    </span>
  );
}
