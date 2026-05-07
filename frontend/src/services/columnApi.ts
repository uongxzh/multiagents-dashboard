import api from "./api";
import type { Column } from "../types/column";

export async function fetchColumns(): Promise<Column[]> {
  const res = await api.get("/columns");
  return res.data;
}
