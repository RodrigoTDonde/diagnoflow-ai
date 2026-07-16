import { useEffect, useMemo, useState } from "react";
import { MockNotice } from "../components/MockNotice";
import { SectionHeader } from "../components/SectionHeader";
import { api } from "../services/api";
import { IncidentWithDiagnostic } from "../types";

export function TechnicalReportPage() {
  const [items, setItems] = useState<IncidentWithDiagnostic[]>([]);
  const [selectedIncidentId, setSelectedIncidentId] = useState<string>("");

  useEffect(() => {
    api.listIncidents().then((response) => {
      setItems(response);
      if (response[0]) {
        setSelectedIncidentId(String(response[0].incident.id));
      }
    });
  }, []);

  const selected = useMemo(
    () => items.find((item) => String(item.incident.id) === selectedIncidentId) ?? null,
    [items, selectedIncidentId],
  );

  return (
    <div className="page">
      <SectionHeader
        title="Relatório técnico"
        description="Selecione uma ocorrência para visualizar o relatório textual consolidado pelo fluxo estruturado da aplicação."
      />
      <MockNotice
        title="Relatório gerado no fluxo atual"
        description="O relatório técnico desta fase é montado a partir do diagnóstico estruturado, das evidências e do checklist da ocorrência selecionada."
      />

      <section className="panel">
        <div className="form-grid">
          <select value={selectedIncidentId} onChange={(e) => setSelectedIncidentId(e.target.value)}>
            {items.length === 0 ? <option value="">Nenhuma ocorrência disponível</option> : null}
            {items.map(({ incident }) => (
              <option key={incident.id} value={incident.id}>
                #{incident.id} • {incident.equipment.name} • {incident.main_symptom}
              </option>
            ))}
          </select>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h3>Conteúdo do relatório</h3>
        </div>
        {selected ? (
          <>
            <textarea className="report-textarea" value={selected.diagnostic.technical_report} readOnly rows={16} />
            <button
              type="button"
              className="secondary-button"
              onClick={() => navigator.clipboard.writeText(selected.diagnostic.technical_report)}
            >
              Copiar relatório técnico
            </button>
          </>
        ) : (
          <p>Nenhum relatório disponível no momento.</p>
        )}
      </section>
    </div>
  );
}
