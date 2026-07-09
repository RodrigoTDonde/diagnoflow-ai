import { useEffect, useState } from "react";
import { MockNotice } from "../components/MockNotice";
import { SectionHeader } from "../components/SectionHeader";
import { api } from "../services/api";
import { AgentRuntime } from "../types";

const tools = [
  "consultar histórico da máquina",
  "consultar base de falhas conhecidas",
  "calcular criticidade",
  "gerar checklist de inspeção",
  "gerar relatório técnico estruturado",
];

export function FutureIntegrationPage() {
  const [runtime, setRuntime] = useState<AgentRuntime | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getAgentRuntime().then(setRuntime).catch((err: Error) => setError(err.message));
  }, []);

  return (
    <div className="page">
      <SectionHeader
        title="Futura integração com IA"
        description="Esta tela documenta como a aplicação poderá evoluir para uma camada real de IA generativa na segunda entrega."
      />
      <MockNotice
        title="Sem integração real nesta etapa"
        description="Esta página continua descritiva na entrega intermediária, mas a branch da fase 2 já expõe a configuração real do orquestrador preparado para a evolução."
      />

      {error ? <section className="panel">Erro ao carregar configuração do agente: {error}</section> : null}

      {runtime ? (
        <section className="panel">
          <div className="panel-header">
            <h3>Configuração atual do agente</h3>
            <span className="badge badge-info">{runtime.runtime_mode}</span>
          </div>

          <div className="agent-runtime-grid">
            <article className="insight-box">
              <strong>Orquestração</strong>
              <p>Runtime: {runtime.runtime_label}</p>
              <p>Estratégia: {runtime.agent_strategy}</p>
              <p>LangGraph ativo: {runtime.use_langgraph ? "sim" : "não"}</p>
            </article>

            <article className="insight-box">
              <strong>Modelo e parâmetros</strong>
              <p>Provider: {runtime.provider}</p>
              <p>Modelo: {runtime.model}</p>
              <p>Temperature: {runtime.temperature}</p>
              <p>Top P: {runtime.top_p}</p>
            </article>

            <article className="insight-box insight-warning">
              <strong>Segurança operacional</strong>
              <p>
                Validação humana para casos de alto risco:{" "}
                {runtime.require_human_validation_for_high_risk ? "obrigatória" : "desativada"}
              </p>
              <p>Esse guardrail impede recomendações críticas sem revisão técnica.</p>
            </article>
          </div>

          <div className="agent-runtime-grid agent-runtime-grid-wide">
            <article className="insight-box">
              <strong>System prompt atual</strong>
              <pre className="agent-pre">{runtime.system_prompt}</pre>
            </article>

            <article className="insight-box">
              <strong>Tools expostas ao agente</strong>
              <ul>
                {runtime.tools.map((tool) => (
                  <li key={tool.name}>
                    <strong>{tool.name}</strong>: {tool.purpose}
                  </li>
                ))}
              </ul>
            </article>
          </div>
        </section>
      ) : null}

      <section className="panel prose">
        <h3>Visão de evolução</h3>
        <p>
          A arquitetura atual já separa serviço de diagnóstico, rotas e tipos, permitindo substituir a lógica mockada por
          uma chamada para LLM sem reescrever o restante do produto.
        </p>
        <p>
          Na branch da fase 2, o backend já foi preparado com orquestrador, tools especializadas, structured output e
          sinalização de validação humana para evoluir o fluxo sem desmontar a base atual.
        </p>

        <h3>Tools previstas</h3>
        <ul>
          {tools.map((tool) => (
            <li key={tool}>{tool}</li>
          ))}
        </ul>

        <h3>Cuidados obrigatórios</h3>
        <p>
          A segunda fase deverá incluir validação humana, trilhas de auditoria, controle de contexto, proteção de dados
          operacionais e mitigação de alucinação antes de qualquer recomendação ser tratada como orientação técnica.
        </p>

        <h3>Limitações atuais</h3>
        <p>
          Nenhum modelo foi integrado nesta etapa. Todas as saídas seguem determinísticas no modo padrão e existem para
          demonstrar a transição segura entre a entrega intermediária e a entrega final.
        </p>
      </section>
    </div>
  );
}
