import { Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { DashboardPage } from "./pages/DashboardPage";
import { EquipmentPage } from "./pages/EquipmentPage";
import { FutureIntegrationPage } from "./pages/FutureIntegrationPage";
import { HistoryPage } from "./pages/HistoryPage";
import { NewIncidentPage } from "./pages/NewIncidentPage";
import { TechnicalReportPage } from "./pages/TechnicalReportPage";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/equipamentos" element={<EquipmentPage />} />
        <Route path="/nova-ocorrencia" element={<NewIncidentPage />} />
        <Route path="/historico" element={<HistoryPage />} />
        <Route path="/relatorio-tecnico" element={<TechnicalReportPage />} />
        <Route path="/futuro-ia" element={<FutureIntegrationPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
