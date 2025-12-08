import http, { setTokens, clearTokens } from "./http.js";

export const registerUser = async (data) => {
  const res = await http.post("/auth/register", data);

  const payload = res.data.payload;
  setTokens({
    token: payload.token,
    refreshToken: payload.refreshToken
  });

  return payload;
};

export const loginUser = async (data) => {
  const res = await http.post("/auth/login", data);

  const payload = res.data.payload;
  setTokens({
    token: payload.token,
    refreshToken: payload.refreshToken
  });

  return payload;
};

export const refreshToken = (token) => {
  return http.get(`/auth/refresh/token?token=${token}`);
};

export const logoutUser = () => {
  clearTokens();
};
