import { MockNotice } from "../components/MockNotice";
import { SectionHeader } from "../components/SectionHeader";

const tools = [
  "consultar histórico da máquina",
  "consultar base de falhas conhecidas",
  "calcular criticidade",
  "gerar checklist de inspeção",
  "gerar relatório técnico estruturado",
];

export function FutureIntegrationPage() {
  return (
    <div className="page">
      <SectionHeader
        title="Futura integração com IA"
        description="Esta tela documenta como a aplicação poderá evoluir para uma camada real de IA generativa na segunda entrega."
      />
      <MockNotice
        title="Sem integração real nesta etapa"
        description="Esta página é apenas descritiva. O comportamento atual da aplicação continua 100% baseado em regras fixas e dados simulados."
      />

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
          Nenhum modelo foi integrado nesta etapa. Todas as saídas são determinísticas, baseadas em regras simples e úteis
          apenas para demonstração funcional da jornada do usuário.
        </p>
      </section>
    </div>
  );
}
