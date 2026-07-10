import { AgentRuntime, DashboardResponse, Equipment, IncidentWithDiagnostic, SymptomFlags } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Erro inesperado." }));
    throw new Error(error.detail ?? "Erro inesperado.");
  }

  return response.json() as Promise<T>;
}

export const api = {
  getAgentRuntime: () => request<AgentRuntime>("/agent/runtime"),
  getDashboard: () => request<DashboardResponse>("/dashboard"),
  listEquipment: () => request<Equipment[]>("/equipment"),
  createEquipment: (payload: Omit<Equipment, "id" | "created_at">) =>
    request<Equipment>("/equipment", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  listIncidents: (params?: { equipmentId?: string; criticality?: string; status?: string }) => {
    const search = new URLSearchParams();
    if (params?.equipmentId) search.set("equipment_id", params.equipmentId);
    if (params?.criticality) search.set("criticality", params.criticality);
    if (params?.status) search.set("status", params.status);
    const query = search.toString();
    return request<IncidentWithDiagnostic[]>(`/incidents${query ? `?${query}` : ""}`);
  },
  createIncident: (payload: {
    equipment_id: number;
    main_symptom: string;
    description: string;
    shift: string;
    perceived_urgency: string;
    status: string;
    symptoms: SymptomFlags;
  }) =>
    request<IncidentWithDiagnostic>("/incidents", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  createHumanReview: (
    incidentId: number,
    payload: {
      reviewer_name: string;
      decision: string;
      notes: string;
    },
  ) =>
    request<IncidentWithDiagnostic["diagnostic"]>(`/diagnostics/${incidentId}/review`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
