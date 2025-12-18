import { useState, useEffect } from 'react';
import CrudPage from '../components/CrudPage';
import {
  gradesService,
  studentsService,
  subjectsService,
  quartersService,
} from '../api/services';

const gradeOptions = [
  { value: 2, label: '2 - Неудовлетворительно' },
  { value: 3, label: '3 - Удовлетворительно' },
  { value: 4, label: '4 - Хорошо' },
  { value: 5, label: '5 - Отлично' },
];

export default function Grades() {
  const [students, setStudents] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [quarters, setQuarters] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [studentsData, subjectsData, quartersData] = await Promise.all([
          studentsService.getAll(),
          subjectsService.getAll(),
          quartersService.getAll(),
        ]);
        setStudents(studentsData.results || studentsData);
        setSubjects(subjectsData.results || subjectsData);
        setQuarters(quartersData.results || quartersData);
      } catch (err) {
        console.error('Error loading data:', err);
      }
    };
    loadData();
  }, []);

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'student_name', label: 'Ученик' },
    { key: 'subject_name', label: 'Предмет' },
    { key: 'quarter_display', label: 'Четверть' },
    {
      key: 'value',
      label: 'Оценка',
      render: (item) => {
        const colors = { 2: '#ef4444', 3: '#f59e0b', 4: '#10b981', 5: '#6366f1' };
        return (
          <span
            style={{
              background: colors[item.value],
              color: 'white',
              padding: '2px 10px',
              borderRadius: '12px',
              fontWeight: 'bold',
            }}
          >
            {item.value}
          </span>
        );
      },
    },
  ];

  const formFields = [
    {
      name: 'student',
      label: 'Ученик',
      type: 'select',
      required: true,
      options: students.map((s) => ({
        value: s.id,
        label: `${s.last_name} ${s.first_name} (${s.school_class_name})`,
      })),
    },
    {
      name: 'subject',
      label: 'Предмет',
      type: 'select',
      required: true,
      options: subjects.map((s) => ({ value: s.id, label: s.name })),
    },
    {
      name: 'quarter',
      label: 'Четверть',
      type: 'select',
      required: true,
      options: quarters.map((q) => ({
        value: q.id,
        label: `${q.number_display} (${q.academic_year})`,
      })),
    },
    {
      name: 'value',
      label: 'Оценка',
      type: 'select',
      required: true,
      options: gradeOptions,
    },
  ];

  return (
    <CrudPage
      title="Оценки"
      icon="⭐"
      service={gradesService}
      columns={columns}
      formFields={formFields}
      initialFormData={{ student: '', subject: '', quarter: '', value: 5 }}
    />
  );
}

