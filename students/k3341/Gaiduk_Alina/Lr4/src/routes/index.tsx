import { Routes, Route, Navigate } from 'react-router-dom'
import { RequireAuth } from '../auth/RequireAuth'
import { AppLayout } from '../layouts/AppLayout'
import { LoginPage } from '../pages/LoginPage'
import { RegisterStaffPage } from '../pages/RegisterStaffPage'
import { ProfilePage } from '../pages/ProfilePage'
import { AuthorsPage } from '../pages/AuthorsPage'
import { PublishersPage } from '../pages/PublishersPage'
import { SectionsPage } from '../pages/SectionsPage'
import { HallsPage } from '../pages/HallsPage'
import { BooksPage } from '../pages/BooksPage'
import { BookDetailPage } from '../pages/BookDetailPage'
import { CopiesPage } from '../pages/CopiesPage'
import { AcceptBookPage } from '../pages/AcceptBookPage'
import { WriteoffBookPage } from '../pages/WriteoffBookPage'
import { StocksPage } from '../pages/StocksPage'
import { ReadersPage } from '../pages/ReadersPage'
import { RegisterReaderPage } from '../pages/RegisterReaderPage'
import { DeactivateReadersPage } from '../pages/DeactivateReadersPage'
import { IssuesPage } from '../pages/IssuesPage'
import { IssueBookPage } from '../pages/IssueBookPage'
import { OverduePage } from '../pages/OverduePage'
import { RareBooksPage } from '../pages/RareBooksPage'
import { AgeStatisticsPage } from '../pages/AgeStatisticsPage'
import { EducationStatisticsPage } from '../pages/EducationStatisticsPage'
import { MonthlyReportPage } from '../pages/MonthlyReportPage'
import { PublisherBooksPage } from '../pages/PublisherBooksPage'
import { HallReadersPage } from '../pages/HallReadersPage'
import { ReaderDetailPage } from '../pages/ReaderDetailPage'
import { ReaderEditPage } from '../pages/ReaderEditPage'

// Компонент с определением всех маршрутов приложения
export const AppRoutes = () => {
  return (
    // Компонент Routes из react-router-dom для определения маршрутов
    <Routes>
      {/* Публичные маршруты (доступны без аутентификации) */}
      <Route path="/login" element={<LoginPage />} />

      {/* Защищенные маршруты (требуют аутентификации) */}
      {/* RequireAuth проверяет наличие токенов, AppLayout предоставляет общий layout */}
      <Route
        element={
          <RequireAuth>
            <AppLayout />
          </RequireAuth>
        }
      >
        {/* Главная страница - перенаправляет на страницу книг */}
        <Route path="/" element={<Navigate to="/books" replace />} />
        {/* Страница профиля пользователя */}
        <Route path="/profile" element={<ProfilePage />} />
        {/* Страница регистрации нового сотрудника */}
        <Route path="/register-staff" element={<RegisterStaffPage />} />

        {/* Справочники (Dictionaries) */}
        {/* Страница со списком авторов */}
        <Route path="/authors" element={<AuthorsPage />} />
        {/* Страница со списком издательств */}
        <Route path="/publishers" element={<PublishersPage />} />
        {/* Страница со списком книг конкретного издательства (динамический параметр :id) */}
        <Route path="/publishers/:id/books" element={<PublisherBooksPage />} />
        {/* Страница со списком разделов книг */}
        <Route path="/sections" element={<SectionsPage />} />
        {/* Страница со списком залов */}
        <Route path="/halls" element={<HallsPage />} />
        {/* Страница со списком читателей конкретного зала (динамический параметр :id) */}
        <Route path="/halls/:id/readers" element={<HallReadersPage />} />

        {/* Книги (Books) */}
        {/* Страница со списком книг */}
        <Route path="/books" element={<BooksPage />} />
        {/* Страница с детальной информацией о книге (динамический параметр :id) */}
        <Route path="/books/:id" element={<BookDetailPage />} />

        {/* Экземпляры книг и остатки (Copies & Stock) */}
        {/* Страница со списком экземпляров книг */}
        <Route path="/copies" element={<CopiesPage />} />
        {/* Страница принятия книги в фонд */}
        <Route path="/accept-book" element={<AcceptBookPage />} />
        {/* Страница списания книги */}
        <Route path="/writeoff-book" element={<WriteoffBookPage />} />
        {/* Страница остатков книг по залам */}
        <Route path="/stocks" element={<StocksPage />} />

        {/* Читатели (Readers) */}
        {/* Страница со списком читателей */}
        <Route path="/readers" element={<ReadersPage />} />
        {/* Страница с детальной информацией о читателе (динамический параметр :id) */}
        <Route path="/readers/:id" element={<ReaderDetailPage />} />
        {/* Страница редактирования читателя (динамический параметр :id) */}
        <Route path="/readers/:id/edit" element={<ReaderEditPage />} />
        {/* Страница регистрации нового читателя */}
        <Route path="/register-reader" element={<RegisterReaderPage />} />
        {/* Страница деактивации старых читателей */}
        <Route path="/deactivate-readers" element={<DeactivateReadersPage />} />

        {/* Выдачи книг (Issues) */}
        {/* Страница со списком выдач книг */}
        <Route path="/issues" element={<IssuesPage />} />
        {/* Страница выдачи книги читателю */}
        <Route path="/issue-book" element={<IssueBookPage />} />

        {/* Аналитика (Analytics) */}
        {/* Страница со списком просроченных выдач */}
        <Route path="/analytics/overdue" element={<OverduePage />} />
        {/* Страница со списком редких книг */}
        <Route path="/analytics/rare-books" element={<RareBooksPage />} />
        {/* Страница со статистикой по возрасту читателей */}
        <Route path="/analytics/age" element={<AgeStatisticsPage />} />
        {/* Страница со статистикой по образованию читателей */}
        <Route path="/analytics/education" element={<EducationStatisticsPage />} />

        {/* Отчеты (Reports) */}
        {/* Страница месячного отчета */}
        <Route path="/reports/monthly" element={<MonthlyReportPage />} />
      </Route>

      {/* Fallback маршрут для всех несуществующих путей - перенаправляет на главную */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

