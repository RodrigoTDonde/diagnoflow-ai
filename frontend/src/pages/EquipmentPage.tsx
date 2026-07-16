import { FormEvent, useEffect, useState } from "react";
import { MockNotice } from "../components/MockNotice";
import { SectionHeader } from "../components/SectionHeader";
import { api } from "../services/api";
import { Equipment } from "../types";

const emptyForm = {
  name: "",
  type: "",
  sector: "",
  manufacturer: "",
  model: "",
  criticality: "média",
  status: "operacional",
};

export function EquipmentPage() {
  const [items, setItems] = useState<Equipment[]>([]);
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState<string | null>(null);

  const loadEquipment = () => {
    api.listEquipment().then(setItems).catch((err: Error) => setError(err.message));
  };

  useEffect(() => {
    loadEquipment();
  }, []);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    try {
      await api.createEquipment({
        ...form,
        name: form.name.trim(),
        type: form.type.trim(),
        sector: form.sector.trim(),
        manufacturer: form.manufacturer.trim(),
        model: form.model.trim(),
      });
      setForm(emptyForm);
      loadEquipment();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível cadastrar o equipamento.");
    }
  };

  return (
    <div className="page split-page">
      <div>
        <SectionHeader
          title="Equipamentos"
          description="Cadastre ativos críticos e mantenha uma base limpa para abrir ocorrências e consolidar histórico técnico."
        />
        <MockNotice
          title="Base operacional simulada"
          description="Os dados persistidos localmente nesta fase existem para sustentar o fluxo da disciplina. Não há enriquecimento por modelo de IA."
        />
        <section className="panel table-panel">
          <div className="panel-header">
            <h3>Ativos cadastrados</h3>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Tipo</th>
                  <th>Setor</th>
                  <th>Criticidade</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.id}>
                    <td>{item.name}</td>
                    <td>{item.type}</td>
                    <td>{item.sector}</td>
                    <td>{item.criticality}</td>
                    <td>{item.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>

      <section className="panel form-panel">
        <div className="panel-header">
          <h3>Novo equipamento</h3>
        </div>
        <form className="form-grid" onSubmit={handleSubmit}>
          {error ? <div className="form-error">{error}</div> : null}
          <input placeholder="Nome do equipamento" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <input placeholder="Tipo" value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })} required />
          <input placeholder="Setor" value={form.sector} onChange={(e) => setForm({ ...form, sector: e.target.value })} required />
          <input
            placeholder="Fabricante"
            value={form.manufacturer}
            onChange={(e) => setForm({ ...form, manufacturer: e.target.value })}
            required
          />
          <input placeholder="Modelo" value={form.model} onChange={(e) => setForm({ ...form, model: e.target.value })} required />
          <select value={form.criticality} onChange={(e) => setForm({ ...form, criticality: e.target.value })}>
            <option value="baixa">Baixa</option>
            <option value="média">Média</option>
            <option value="alta">Alta</option>
          </select>
          <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
            <option value="operacional">Operacional</option>
            <option value="em observação">Em observação</option>
            <option value="operando com restrição">Operando com restrição</option>
            <option value="parado">Parado</option>
          </select>
          <button type="submit">Cadastrar equipamento</button>
        </form>
      </section>
    </div>
  );
}
