import { http } from "./http";

// POST /auth/token (OAuth2PasswordRequestForm)
// отправляем username/password как application/x-www-form-urlencoded
export async function login(username, password) {
  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);

  const res = await http.post("/auth/token", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  // ожидаем { access_token, token_type }
  return res.data;
}


// POST /auth/register (JSON)
export async function register(username, password) {
  const res = await http.post("/auth/register", { username, password });
  return res.data; // вернёт пользователя (по твоему бэку response_model=UserOut)
}

export async function getMe() {
  const res = await http.get("/auth/me");
  return res.data;
}

export async function updateMe(payload) {
  const res = await http.patch("/auth/me", payload);
  return res.data;
}
