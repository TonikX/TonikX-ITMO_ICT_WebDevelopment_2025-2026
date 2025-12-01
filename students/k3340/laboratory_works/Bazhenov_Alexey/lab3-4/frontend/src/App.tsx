import { Route, Routes } from 'react-router-dom';

import { DashboardLayout } from './components/DashboardLayout';
import { ClientsPage } from './pages/ClientsPage';
import { DashboardPage } from './pages/DashboardPage';
import { EmployeesPage } from './pages/EmployeesPage';
import { ReportsPage } from './pages/ReportsPage';
import { RoomsPage } from './pages/RoomsPage';
import { StaysPage } from './pages/StaysPage';

export function App() {
  return (
    <DashboardLayout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/rooms" element={<RoomsPage />} />
        <Route path="/clients" element={<ClientsPage />} />
        <Route path="/stays" element={<StaysPage />} />
        <Route path="/employees" element={<EmployeesPage />} />
        <Route path="/reports" element={<ReportsPage />} />
      </Routes>
    </DashboardLayout>
  );
}

export default App;
