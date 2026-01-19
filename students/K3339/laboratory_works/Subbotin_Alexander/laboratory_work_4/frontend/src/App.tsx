import { useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';

import { Layout } from '@/components/layout';
import { PrivateRoute } from '@/components/PrivateRoute';
import {
  HomePage,
  LoginPage,
  RegisterPage,
  ProfilePage,
  ToursPage,
  TourDetailPage,
  TourFormPage,
  ReservationsPage,
  AdminReservationsPage,
  TermsPage,
} from '@/pages';
import { useAuthStore } from '@/store';

function App() {
  const { fetchUser, token } = useAuthStore();

  useEffect(() => {
    // Если есть токен, пробуем получить данные пользователя
    if (token) {
      fetchUser();
    }
  }, [fetchUser, token]);

  return (
    <Layout>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/tours" element={<ToursPage />} />
        <Route path="/tours/:id" element={<TourDetailPage />} />
        <Route path="/terms" element={<TermsPage />} />

        {/* Protected routes */}
        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <ProfilePage />
            </PrivateRoute>
          }
        />
        <Route
          path="/tours/new"
          element={
            <PrivateRoute>
              <TourFormPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/tours/:id/edit"
          element={
            <PrivateRoute>
              <TourFormPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/reservations"
          element={
            <PrivateRoute>
              <ReservationsPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/admin/reservations"
          element={
            <PrivateRoute>
              <AdminReservationsPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </Layout>
  );
}

export default App;
