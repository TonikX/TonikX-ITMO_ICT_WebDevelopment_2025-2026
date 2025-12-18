import { useState, useEffect } from 'react';
import {
  subjectsService,
  classroomsService,
  teachersService,
  schoolClassesService,
  studentsService,
  quartersService,
} from '../api/services';
import '../styles/dashboard.css';

export default function Dashboard() {
  const [stats, setStats] = useState({
    subjects: 0,
    classrooms: 0,
    teachers: 0,
    classes: 0,
    students: 0,
  });
  const [genderStats, setGenderStats] = useState([]);
  const [teacherCount, setTeacherCount] = useState([]);
  const [classroomTypes, setClassroomTypes] = useState([]);
  const [currentQuarter, setCurrentQuarter] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [subjects, classrooms, teachers, classes, students] = await Promise.all([
        subjectsService.getAll(),
        classroomsService.getAll(),
        teachersService.getAll(),
        schoolClassesService.getAll(),
        studentsService.getAll(),
      ]);

      setStats({
        subjects: subjects.count || subjects.results?.length || subjects.length || 0,
        classrooms: classrooms.count || classrooms.results?.length || classrooms.length || 0,
        teachers: teachers.count || teachers.results?.length || teachers.length || 0,
        classes: classes.count || classes.results?.length || classes.length || 0,
        students: students.count || students.results?.length || students.length || 0,
      });

      // Load additional stats
      const [genderData, teacherCountData, classroomTypesData] = await Promise.all([
        schoolClassesService.getGenderStats(),
        subjectsService.getTeacherCount(),
        classroomsService.getTypeCount(),
      ]);

      setGenderStats(genderData);
      setTeacherCount(teacherCountData);
      setClassroomTypes(classroomTypesData);

      // Try to get current quarter
      try {
        const quarter = await quartersService.getCurrent();
        setCurrentQuarter(quarter);
      } catch (e) {
        // No current quarter set
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner"></div>
        <p>Загрузка данных...</p>
      </div>
    );
  }

  const statCards = [
    { label: 'Предметов', value: stats.subjects, icon: '📚', color: '#6366f1' },
    { label: 'Кабинетов', value: stats.classrooms, icon: '🚪', color: '#8b5cf6' },
    { label: 'Учителей', value: stats.teachers, icon: '👨‍🏫', color: '#ec4899' },
    { label: 'Классов', value: stats.classes, icon: '👥', color: '#f59e0b' },
    { label: 'Учеников', value: stats.students, icon: '🎓', color: '#10b981' },
  ];

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1>📊 Панель управления</h1>
        {currentQuarter && (
          <div className="current-quarter">
            <span className="quarter-badge">{currentQuarter.number_display}</span>
            <span className="quarter-year">{currentQuarter.academic_year}</span>
          </div>
        )}
      </div>

      <div className="stats-grid">
        {statCards.map((card) => (
          <div key={card.label} className="stat-card" style={{ '--accent-color': card.color }}>
            <div className="stat-icon">{card.icon}</div>
            <div className="stat-info">
              <span className="stat-value">{card.value}</span>
              <span className="stat-label">{card.label}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>👦👧 Статистика по полу в классах</h3>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Класс</th>
                  <th>Мальчики</th>
                  <th>Девочки</th>
                  <th>Всего</th>
                </tr>
              </thead>
              <tbody>
                {genderStats.map((item, index) => (
                  <tr key={index}>
                    <td>{item.school_class}</td>
                    <td>{item.boys_count}</td>
                    <td>{item.girls_count}</td>
                    <td>{item.total}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="dashboard-card">
          <h3>👨‍🏫 Учителей по предметам</h3>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Предмет</th>
                  <th>Количество учителей</th>
                </tr>
              </thead>
              <tbody>
                {teacherCount.map((item, index) => (
                  <tr key={index}>
                    <td>{item.subject}</td>
                    <td>{item.teachers_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="dashboard-card small">
          <h3>🚪 Кабинеты по типам</h3>
          <div className="type-stats">
            {classroomTypes.map((item, index) => (
              <div key={index} className="type-stat-item">
                <span className="type-name">{item.classroom_type}</span>
                <span className="type-count">{item.count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

