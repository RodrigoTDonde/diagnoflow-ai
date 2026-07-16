import { useEffect, useState } from "react";
import { MockNotice } from "../components/MockNotice";
import { SectionHeader } from "../components/SectionHeader";
import { StatCard } from "../components/StatCard";
import { api } from "../services/api";
import { DashboardResponse } from "../types";

export function DashboardPage() {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getDashboard().then(setData).catch((err: Error) => setError(err.message));
  }, []);

  if (error) {
    return <div className="panel">Erro ao carregar o painel operacional: {error}</div>;
  }

  if (!data) {
    return <div className="panel">Carregando indicadores operacionais...</div>;
  }

  return (
    <div className="page">
      <SectionHeader
        title="Painel operacional"
        description="Visão rápida da planta, com alertas críticos, ocorrências abertas e diagnósticos estruturados mais recentes."
      />

      <section className="hero-card">
        <div>
          <span className="badge badge-info">Entrega final em demonstração</span>
          <h3>Triagem técnica assistida com runtime estruturado e validação humana</h3>
        </div>
        <p>Aplicação pronta para demonstração local, com integração validada no runtime da fase 2.</p>
      </section>

      {data.latest_incidents[0]?.diagnostic ? (
        <section className="phase2-card">
          <div className="phase2-card-head">
            <strong>Camada de evolução da fase 2</strong>
            <span className="badge badge-info">{data.latest_incidents[0].diagnostic.runtime_mode ?? "fallback-local"}</span>
          </div>
          <p>
            Runtime atual: <strong>{data.latest_incidents[0].diagnostic.runtime_label ?? "fallback-local"}</strong>
          </p>
          <p>
            Provider: <strong>{data.latest_incidents[0].diagnostic.runtime_provider ?? "not-configured"}</strong> • Modelo:{" "}
            <strong>{data.latest_incidents[0].diagnostic.runtime_model ?? "diagnoflow-mock-agent"}</strong>
          </p>
        </section>
      ) : null}

      <MockNotice
        badgeLabel="Entrega final"
        title="Fluxo assistido com arquitetura da fase 2"
        description="A aplicação já expõe runtime, tools, output estruturado e revisão humana para demonstrar a evolução técnica da entrega final."
      />

      <section className="stat-grid">
        <StatCard label="Equipamentos cadastrados" value={data.summary.total_equipment} />
        <StatCard label="Ocorrências abertas" value={data.summary.open_incidents} tone="alert" />
        <StatCard label="Alertas críticos" value={data.summary.critical_alerts} tone="danger" />
        <StatCard label="Diagnósticos estruturados" value={data.summary.simulated_diagnostics} />
      </section>

      <section className="panel">
        <div className="panel-header">
          <h3>Últimas ocorrências</h3>
        </div>
        <div className="incident-list">
          {data.latest_incidents.map(({ incident, diagnostic }) => (
            <article key={incident.id} className="incident-card">
              <div className="incident-card-head">
                <div>
                  <h4>{incident.equipment.name}</h4>
                  <p>
                    {incident.main_symptom} • {incident.shift}
                  </p>
                </div>
                <span className={`badge badge-${diagnostic.priority}`}>{diagnostic.priority}</span>
              </div>
              <p>{diagnostic.probable_cause}</p>
              {diagnostic.requires_human_validation ? (
                <p className="incident-note">Requer validação humana antes de ação crítica.</p>
              ) : null}
              {diagnostic.evidence_summary?.length ? <p className="incident-note">Baseado em: {diagnostic.evidence_summary[0]}</p> : null}
              <small>{new Date(incident.created_at).toLocaleString("pt-BR")}</small>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
