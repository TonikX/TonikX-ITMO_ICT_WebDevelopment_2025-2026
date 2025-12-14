import { useState, useEffect } from 'react';
import CrudPage from '../components/CrudPage';
import { studentsService, schoolClassesService } from '../api/services';

export default function Students() {
  const [classes, setClasses] = useState([]);

  useEffect(() => {
    const loadClasses = async () => {
      try {
        const data = await schoolClassesService.getAll();
        setClasses(data.results || data);
      } catch (err) {
        console.error('Error loading classes:', err);
      }
    };
    loadClasses();
  }, []);

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'last_name', label: 'Фамилия' },
    { key: 'first_name', label: 'Имя' },
    { key: 'gender_display', label: 'Пол' },
    { key: 'school_class_name', label: 'Класс' },
  ];

  const formFields = [
    { name: 'first_name', label: 'Имя', type: 'text', required: true },
    { name: 'last_name', label: 'Фамилия', type: 'text', required: true },
    {
      name: 'gender',
      label: 'Пол',
      type: 'select',
      required: true,
      options: [
        { value: 'M', label: 'Мужской' },
        { value: 'F', label: 'Женский' },
      ],
    },
    {
      name: 'school_class',
      label: 'Класс',
      type: 'select',
      required: true,
      options: classes.map((c) => ({ value: c.id, label: c.name })),
    },
  ];

  return (
    <CrudPage
      title="Ученики"
      icon="🎓"
      service={studentsService}
      columns={columns}
      formFields={formFields}
      initialFormData={{ first_name: '', last_name: '', gender: 'M', school_class: '' }}
    />
  );
}

