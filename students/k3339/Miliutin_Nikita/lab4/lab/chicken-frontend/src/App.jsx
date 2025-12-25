import { Navigate, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Chickens from "./pages/Chickens";
import { getToken } from "./utils/token";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Dashboard from "./pages/Dashboard";
import Workshops from "./pages/Workshops";
import WorkshopDetail from "./pages/WorkshopDetail";
import CageDetail from "./pages/CageDetail";
import ChickenMove from "./pages/ChickenMove";
import ChickenDetail from "./pages/ChickenDetail";
import EmployeesPage from "./pages/EmployeesPage";
import EmployeeDetail from "./pages/EmployeeDetail";
import EmployeeCreate from "./pages/EmployeeCreate";
import DietsPage from "./pages/DietsPage";
import DietDetail from "./pages/DietDetail";
import DietCreate from "./pages/DietCreate";
import AppShell from "./components/AppShell";

function RequireAuth({ children }) {
  const token = getToken();
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/"
          element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          }
        />

        <Route
          path="/profile"
          element={
            <RequireAuth>
              <Profile />
            </RequireAuth>
          }
        />

        <Route
          path="/chickens"
          element={
            <RequireAuth>
              <Chickens />
            </RequireAuth>
          }
        />

        <Route
          path="/chickens/:chickenId"
          element={
            <RequireAuth>
              <ChickenDetail />
            </RequireAuth>
          }
        />

        <Route
          path="/chickens/:chickenId/move"
          element={
            <RequireAuth>
              <ChickenMove />
            </RequireAuth>
          }
        />

        <Route
          path="/workshops"
          element={
            <RequireAuth>
              <Workshops />
            </RequireAuth>
          }
        />

        <Route
          path="/workshops/:workshopId"
          element={
            <RequireAuth>
              <WorkshopDetail />
            </RequireAuth>
          }
        />

        <Route
          path="/cages/:cageId"
          element={
            <RequireAuth>
              <CageDetail />
            </RequireAuth>
          }
        />

        <Route
          path="/employees"
          element={
            <RequireAuth>
              <EmployeesPage />
            </RequireAuth>
          }
        />

        <Route
          path="/employees/new"
          element={
            <RequireAuth>
              <EmployeeCreate />
            </RequireAuth>
          }
        />

        <Route
          path="/employees/:employeeId"
          element={
            <RequireAuth>
              <EmployeeDetail />
            </RequireAuth>
          }
        />

        <Route
          path="/diets"
          element={
            <RequireAuth>
              <DietsPage />
            </RequireAuth>
          }
        />

        <Route
          path="/diets/new"
          element={
            <RequireAuth>
              <DietCreate />
            </RequireAuth>
          }
        />

        <Route
          path="/diets/:dietId"
          element={
            <RequireAuth>
              <DietDetail />
            </RequireAuth>
          }
        />

        {/* по умолчанию */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppShell>
  );
}
