import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="container">
      <div className="dash-wrap">
        <div className="dash-card">
          <h1 className="dash-title">Панель</h1>
          <div className="dash-sub">Куда идём?</div>

          <div className="dash-menu">
            <Link to="/diets" className="dash-item">🥣 Диеты</Link>
            <Link to="/workshops" className="dash-item">🏭 Цеха</Link>
            <Link to="/employees" className="dash-item">👷 Работники</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
