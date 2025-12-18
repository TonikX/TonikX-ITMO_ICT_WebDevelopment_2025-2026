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

// компонент с определением всех маршрутов приложения
export const AppRoutes = () => {
  return (
    <Routes>
      {/* публичные маршруты (доступны без аутентификации) */}
      <Route path="/login" element={<LoginPage />} />

      {/* защищенные маршруты (требуют аутентификации) */}
      {/* RequireAuth проверяет наличие токенов, AppLayout предоставляет общий layout */}
      <Route
        element={
          <RequireAuth>
            <AppLayout />
          </RequireAuth>
        }
      >
        {/* главная страница - перенаправляет на страницу книг */}
        <Route path="/" element={<Navigate to="/books" replace />} />
        {/* страница профиля пользователя */}
        <Route path="/profile" element={<ProfilePage />} />
        {/* страница регистрации нового сотрудника */}
        <Route path="/register-staff" element={<RegisterStaffPage />} />

        {/* страница со списком авторов */}
        <Route path="/authors" element={<AuthorsPage />} />
        {/* страница со списком издательств */}
        <Route path="/publishers" element={<PublishersPage />} />
        {/* страница со списком книг конкретного издательства (динамический параметр :id) */}
        <Route path="/publishers/:id/books" element={<PublisherBooksPage />} />
        {/* страница со списком разделов книг */}
        <Route path="/sections" element={<SectionsPage />} />
        {/* страница со списком залов */}
        <Route path="/halls" element={<HallsPage />} />
        {/* страница со списком читателей конкретного зала (динамический параметр :id) */}
        <Route path="/halls/:id/readers" element={<HallReadersPage />} />

        {/* книги */}
        {/* страница со списком книг */}
        <Route path="/books" element={<BooksPage />} />
        {/* страница с детальной информацией о книге (динамический параметр :id) */}
        <Route path="/books/:id" element={<BookDetailPage />} />

        {/* экземпляры книг и остатки (Copies & Stock) */}
        {/* страница со списком экземпляров книг */}
        <Route path="/copies" element={<CopiesPage />} />
        {/* страница принятия книги в фонд */}
        <Route path="/accept-book" element={<AcceptBookPage />} />
        {/* страница списания книги */}
        <Route path="/writeoff-book" element={<WriteoffBookPage />} />
        {/* страница остатков книг по залам */}
        <Route path="/stocks" element={<StocksPage />} />

        {/* читатели */}
        {/* страница со списком читателей */}
        <Route path="/readers" element={<ReadersPage />} />
        {/* страница с детальной информацией о читателе (динамический параметр :id) */}
        <Route path="/readers/:id" element={<ReaderDetailPage />} />
        {/* страница редактирования читателя (динамический параметр :id) */}
        <Route path="/readers/:id/edit" element={<ReaderEditPage />} />
        {/* страница регистрации нового читателя */}
        <Route path="/register-reader" element={<RegisterReaderPage />} />
        {/* страница деактивации старых читателей */}
        <Route path="/deactivate-readers" element={<DeactivateReadersPage />} />

        {/* выдачи */}
        {/* страница со списком выдач книг */}
        <Route path="/issues" element={<IssuesPage />} />
        {/* страница выдачи книги читателю */}
        <Route path="/issue-book" element={<IssueBookPage />} />

        {/* аналитика */}
        {/* страница со списком просроченных выдач */}
        <Route path="/analytics/overdue" element={<OverduePage />} />
        {/* страница со списком редких книг */}
        <Route path="/analytics/rare-books" element={<RareBooksPage />} />
        {/* страница со статистикой по возрасту читателей */}
        <Route path="/analytics/age" element={<AgeStatisticsPage />} />
        {/* страница со статистикой по образованию читателей */}
        <Route path="/analytics/education" element={<EducationStatisticsPage />} />

        {/* отчет */}
        <Route path="/reports/monthly" element={<MonthlyReportPage />} />
      </Route>

      {/* маршрут для всех несуществующих путей - перенаправляет на главную */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

