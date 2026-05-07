import api from "./api";
import type { Agent } from "../types/agent";

export async function fetchAgents(): Promise<Agent[]> {
  const res = await api.get("/agents");
  return res.data;
}

export async function fetchAgent(id: string): Promise<Agent> {
  const res = await api.get(`/agents/${id}`);
  return res.data;
}
