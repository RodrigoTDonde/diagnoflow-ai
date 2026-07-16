import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  { to: "/", label: "Painel" },
  { to: "/equipamentos", label: "Equipamentos" },
  { to: "/nova-ocorrencia", label: "Nova Ocorrência" },
  { to: "/historico", label: "Histórico" },
  { to: "/relatorio-tecnico", label: "Relatório Técnico" },
  { to: "/futuro-ia", label: "Futura IA" },
];

export function Layout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-stack">
          <div className="sidebar-brand">
            <p className="eyebrow">DiagnoFlow AI</p>
            <h1>Triagem técnica industrial</h1>
            <p className="sidebar-copy">
              Plataforma de apoio para registrar sintomas, organizar ocorrências e emitir diagnósticos técnicos estruturados.
            </p>
          </div>

          <div className="sidebar-section">
            <p className="sidebar-label">Navegação</p>
            <nav className="nav">
              {navItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </div>

          <div className="sidebar-footer">
            <span className="badge badge-warning">Fase 2 ativa</span>
            <p>Fluxo com runtime configurável, tools locais, output estruturado e validação humana.</p>
          </div>
        </div>
      </aside>

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
