import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Subjects from './pages/Subjects';
import Classrooms from './pages/Classrooms';
import Teachers from './pages/Teachers';
import SchoolClasses from './pages/SchoolClasses';
import Students from './pages/Students';
import Quarters from './pages/Quarters';
import TeachingAssignments from './pages/TeachingAssignments';
import Schedule from './pages/Schedule';
import Grades from './pages/Grades';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="subjects" element={<Subjects />} />
            <Route path="classrooms" element={<Classrooms />} />
            <Route path="teachers" element={<Teachers />} />
            <Route path="classes" element={<SchoolClasses />} />
            <Route path="students" element={<Students />} />
            <Route path="quarters" element={<Quarters />} />
            <Route path="assignments" element={<TeachingAssignments />} />
            <Route path="schedule" element={<Schedule />} />
            <Route path="grades" element={<Grades />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
