import { api, authApi } from './axios';

export default {
    // Пользователи
    getUsers() {
        return authApi.get('/users/');
    },

    // Авторы
    getAuthors() {
        return api.get('/authors/');
    },
    getAuthor(id) {
        return api.get(`/authors/${id}/`);
    },
    createAuthor(data) {
        return api.post('/authors/', data);
    },
    updateAuthor(id, data) {
        return api.put(`/authors/${id}/`, data);
    },
    deleteAuthor(id) {
        return api.delete(`/authors/${id}/`);
    },

    // Книги
    getBooks(params = {}) {
        return api.get('/books/', { params });
    },
    getBook(id) {
        return api.get(`/books/${id}/`);
    },
    createBook(data) {
        return api.post('/books/', data);
    },
    updateBook(id, data) {
        return api.put(`/books/${id}/`, data);
    },
    deleteBook(id) {
        return api.delete(`/books/${id}/`);
    },
    getBooksWithStats() {
        return api.get('/books/with_stats/');
    },

    // Контракты
    getContracts() {
        return api.get('/contracts/');
    },
    getContract(id) {
        return api.get(`/contracts/${id}/`);
    },
    createContract(data) {
        return api.post('/contracts/', data);
    },
    updateContract(id, data) {
        return api.put(`/contracts/${id}/`, data);
    },
    deleteContract(id) {
        return api.delete(`/contracts/${id}/`);
    },

    // Отчеты
    getQuarterlyReport() {
        return api.get('/contracts/quarterly_report/');
    },
    getTopManagers(start, end) {
        return api.get('/contracts/top_managers/', { params: { start, end } });
    },
    getYearlyStats() {
        return api.get('/contracts/yearly_stats/');
    },

    // Вспомогательные методы
    getCustomers() {
        return api.get('/customers/');
    },

    // Авторы книг
    getBookAuthors(bookId) {
        return api.get('/book-authors/', { params: { book: bookId } });
    },
    createBookAuthor(data) {
        return api.post('/book-authors/', data);
    },
    deleteBookAuthor(id) {
        return api.delete(`/book-authors/${id}/`);
    }
};
