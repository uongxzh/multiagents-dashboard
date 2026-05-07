interface EmptyStateProps {
  icon?: string;
  title: string;
  description?: string;
}

export default function EmptyState({ icon = "📭", title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <span className="text-4xl">{icon}</span>
      <h3 className="mt-4 text-lg font-medium text-white">{title}</h3>
      {description && <p className="mt-1 text-sm text-surface-400">{description}</p>}
    </div>
  );
}
