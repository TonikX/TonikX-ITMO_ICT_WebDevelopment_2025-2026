import { useNavigate, Link } from "react-router-dom";
import { clearToken } from "../utils/token";

export default function Chickens() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: 20 }}>
      <h2>Chickens (заглушка)</h2>

      <p>
          <Link to="/profile">Перейти в профиль</Link>
      </p>

      <p>Если ты здесь — значит логин прошёл и токен сохранён.</p>

      <button
        onClick={() => {
          clearToken();
          navigate("/login");
        }}
      >
        Выйти
      </button>
    </div>
  );
}
