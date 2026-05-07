export interface Agent {
  id: string;
  name: string;
  role: string;
  description: string | null;
  runtime_id: string | null;
  environment: string;
  status: "idle" | "working" | "offline" | "online";
  avatar: string | null;
  created_at: string | null;
}
