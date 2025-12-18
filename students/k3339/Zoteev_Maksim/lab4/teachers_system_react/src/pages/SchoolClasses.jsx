import { useState, useEffect } from 'react';
import CrudPage from '../components/CrudPage';
import { schoolClassesService, teachersService } from '../api/services';

export default function SchoolClasses() {
  const [teachers, setTeachers] = useState([]);

  useEffect(() => {
    const loadTeachers = async () => {
      try {
        const data = await teachersService.getAll();
        setTeachers(data.results || data);
      } catch (err) {
        console.error('Error loading teachers:', err);
      }
    };
    loadTeachers();
  }, []);

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Класс' },
    {
      key: 'class_teacher',
      label: 'Классный руководитель',
      render: (item) => {
        const teacher = teachers.find((t) => t.id === item.class_teacher);
        return teacher ? teacher.full_name : '—';
      },
    },
  ];

  const formFields = [
    {
      name: 'number',
      label: 'Номер класса',
      type: 'select',
      required: true,
      options: Array.from({ length: 11 }, (_, i) => ({
        value: i + 1,
        label: String(i + 1),
      })),
    },
    {
      name: 'letter',
      label: 'Буква класса',
      type: 'select',
      required: true,
      options: ['А', 'Б', 'В', 'Г', 'Д'].map((l) => ({ value: l, label: l })),
    },
    {
      name: 'class_teacher',
      label: 'Классный руководитель',
      type: 'select',
      required: false,
      options: teachers.map((t) => ({ value: t.id, label: t.full_name })),
    },
  ];

  return (
    <CrudPage
      title="Классы"
      icon="👥"
      service={schoolClassesService}
      columns={columns}
      formFields={formFields}
      initialFormData={{ number: 1, letter: 'А', class_teacher: '' }}
    />
  );
}

