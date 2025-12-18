import { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, logout as apiLogout, getCurrentUser, register as apiRegister } from '../api/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const userData = await getCurrentUser(token);
          setUser(userData);
        } catch (error) {
          localStorage.removeItem('authToken');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };
    checkAuth();
  }, [token]);

  const login = async (username, password) => {
    const data = await apiLogin(username, password);
    const authToken = data.auth_token;
    localStorage.setItem('authToken', authToken);
    setToken(authToken);
    const userData = await getCurrentUser(authToken);
    setUser(userData);
    return data;
  };

  const register = async (username, password, re_password) => {
    await apiRegister(username, password, re_password);
    // After registration, log in automatically
    return await login(username, password);
  };

  const logout = async () => {
    if (token) {
      try {
        await apiLogout(token);
      } catch (error) {
        // Ignore logout errors
      }
    }
    localStorage.removeItem('authToken');
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated: !!token && !!user,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

