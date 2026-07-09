import { FormEvent, useEffect, useMemo, useState } from "react";
import { MockNotice } from "../components/MockNotice";
import { SectionHeader } from "../components/SectionHeader";
import { api } from "../services/api";
import { Equipment, IncidentWithDiagnostic, SymptomFlags } from "../types";

const initialSymptoms: SymptomFlags = {
  abnormal_noise: false,
  vibration: false,
  overheating: false,
  leakage: false,
  electrical_failure: false,
  total_stop: false,
  performance_loss: false,
};

export function NewIncidentPage() {
  const [equipment, setEquipment] = useState<Equipment[]>([]);
  const [result, setResult] = useState<IncidentWithDiagnostic | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    equipment_id: "",
    main_symptom: "",
    description: "",
    shift: "manhã",
    perceived_urgency: "média",
    status: "open",
  });
  const [symptoms, setSymptoms] = useState<SymptomFlags>(initialSymptoms);

  useEffect(() => {
    api.listEquipment().then(setEquipment).catch((err: Error) => setError(err.message));
  }, []);

  const selectedEquipment = useMemo(
    () => equipment.find((item) => item.id === Number(form.equipment_id)),
    [equipment, form.equipment_id],
  );

  const toggleSymptom = (key: keyof SymptomFlags) => {
    setSymptoms((current) => ({ ...current, [key]: !current[key] }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    try {
      const payload = {
        ...form,
        equipment_id: Number(form.equipment_id),
        symptoms,
      };
      const response = await api.createIncident(payload);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao registrar ocorrencia.");
    }
  };

  return (
    <div className="page split-page">
      <div>
        <SectionHeader
          title="Nova ocorrência"
          description="Registre sintomas operacionais e receba um diagnóstico técnico simulado baseado em regras simples."
        />
        <MockNotice
          title="Fluxo mockado para demonstração"
          description="Ao enviar a ocorrência, o sistema gera uma resposta determinística com base nos sintomas informados. Nenhum modelo generativo participa deste processo."
        />
        <section className="panel">
          <form className="form-grid" onSubmit={handleSubmit}>
            {error ? <div className="form-error">{error}</div> : null}
            <select value={form.equipment_id} onChange={(e) => setForm({ ...form, equipment_id: e.target.value })} required>
              <option value="">Selecione o equipamento</option>
              {equipment.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.name}
                </option>
              ))}
            </select>
            <input
              placeholder="Sintoma principal"
              value={form.main_symptom}
              onChange={(e) => setForm({ ...form, main_symptom: e.target.value })}
              required
            />
            <textarea
              placeholder="Descrição operacional"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              rows={5}
              required
            />
            <select value={form.shift} onChange={(e) => setForm({ ...form, shift: e.target.value })}>
              <option value="manhã">Manhã</option>
              <option value="tarde">Tarde</option>
              <option value="noite">Noite</option>
            </select>
            <select value={form.perceived_urgency} onChange={(e) => setForm({ ...form, perceived_urgency: e.target.value })}>
              <option value="baixa">Baixa</option>
              <option value="média">Média</option>
              <option value="alta">Alta</option>
            </select>

            <div className="checkbox-grid">
              {[
                ["abnormal_noise", "Ruído anormal"],
                ["vibration", "Vibração"],
                ["overheating", "Superaquecimento"],
                ["leakage", "Vazamento"],
                ["electrical_failure", "Falha elétrica"],
                ["total_stop", "Parada total"],
                ["performance_loss", "Perda de desempenho"],
              ].map(([key, label]) => (
                <label key={key} className="checkbox-card">
                  <input
                    type="checkbox"
                    checked={symptoms[key as keyof SymptomFlags]}
                    onChange={() => toggleSymptom(key as keyof SymptomFlags)}
                  />
                  <span>{label}</span>
                </label>
              ))}
            </div>
            <button type="submit">Gerar diagnóstico simulado</button>
          </form>
        </section>
      </div>

      <section className="panel result-panel">
        <div className="panel-header">
          <h3>Saída do diagnóstico</h3>
        </div>
        {result ? (
          <>
            <span className="badge badge-warning">Diagnóstico simulado - nenhum LLM foi integrado nesta fase.</span>
            <div className="phase2-card">
              <div className="phase2-card-head">
                <strong>Modo da fase 2</strong>
                <span className="badge badge-info">{result.diagnostic.runtime_mode ?? "fallback-local"}</span>
              </div>
              <p>
                Runtime: <strong>{result.diagnostic.runtime_label ?? "fallback-local"}</strong>
              </p>
              <p>
                Provider: <strong>{result.diagnostic.runtime_provider ?? "not-configured"}</strong> • Modelo:{" "}
                <strong>{result.diagnostic.runtime_model ?? "diagnoflow-mock-agent"}</strong>
              </p>
            </div>
            <h4>{result.diagnostic.probable_cause}</h4>
            <p>
              Equipamento: <strong>{selectedEquipment?.name ?? result.incident.equipment.name}</strong>
            </p>
            <p>Confiança simulada: {Math.round(result.diagnostic.confidence_level * 100)}%</p>
            <p>Prioridade: {result.diagnostic.priority}</p>
            <p>Risco operacional: {result.diagnostic.operational_risk}</p>
            {result.diagnostic.requires_human_validation ? (
              <div className="insight-box insight-warning">
                <strong>Validação humana recomendada</strong>
                <p>Este caso deve ser revisado por um responsável técnico antes de qualquer decisão crítica.</p>
              </div>
            ) : null}
            <p>Observações: {result.diagnostic.observations}</p>
            <div>
              <strong>Ações recomendadas</strong>
              <ul>
                {result.diagnostic.recommended_actions.map((action) => (
                  <li key={action}>{action}</li>
                ))}
              </ul>
            </div>
            <div>
              <strong>Peças possivelmente envolvidas</strong>
              <p>{result.diagnostic.involved_parts.join(", ")}</p>
            </div>
            {result.diagnostic.evidence_summary?.length ? (
              <div className="insight-box">
                <strong>Evidências consideradas</strong>
                <ul>
                  {result.diagnostic.evidence_summary.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ) : null}
            {result.diagnostic.missing_information?.length ? (
              <div className="insight-box">
                <strong>Lacunas de contexto</strong>
                <ul>
                  {result.diagnostic.missing_information.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ) : null}
            {result.diagnostic.inspection_checklist?.length ? (
              <div className="insight-box">
                <strong>Checklist de inspeção</strong>
                <ul>
                  {result.diagnostic.inspection_checklist.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ) : null}
            <button
              type="button"
              className="secondary-button"
              onClick={() => navigator.clipboard.writeText(result.diagnostic.technical_report)}
            >
              Copiar relatório técnico
            </button>
          </>
        ) : (
          <p>Preencha o formulário para gerar uma análise mockada e um relatório textual reutilizável.</p>
        )}
      </section>
    </div>
  );
}
