// token.ts

const TOKEN_KEY = 'token';  // Ключ для хранения токена в localStorage

export default {
    getToken(): string | null {
        return localStorage.getItem(TOKEN_KEY);
    },
    setToken(token: string): void {
        localStorage.setItem(TOKEN_KEY, token);
    },
    removeToken(): void {
        localStorage.removeItem(TOKEN_KEY);
    },
    isAuthenticated(): boolean {
        return !!this.getToken();
    },
};
