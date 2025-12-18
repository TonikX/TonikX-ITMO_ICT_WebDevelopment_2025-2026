import { useState, useEffect } from 'react';
import CrudPage from '../components/CrudPage';
import { teachersService, classroomsService } from '../api/services';

export default function Teachers() {
  const [classrooms, setClassrooms] = useState([]);

  useEffect(() => {
    const loadClassrooms = async () => {
      try {
        const data = await classroomsService.getAll();
        setClassrooms(data.results || data);
      } catch (err) {
        console.error('Error loading classrooms:', err);
      }
    };
    loadClassrooms();
  }, []);

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'full_name', label: 'ФИО' },
    {
      key: 'classroom',
      label: 'Кабинет',
      render: (item) => {
        const classroom = classrooms.find((c) => c.id === item.classroom);
        return classroom ? classroom.number : '—';
      },
    },
  ];

  const formFields = [
    { name: 'first_name', label: 'Имя', type: 'text', required: true },
    { name: 'last_name', label: 'Фамилия', type: 'text', required: true },
    { name: 'patronymic', label: 'Отчество', type: 'text', required: false },
    {
      name: 'classroom',
      label: 'Кабинет',
      type: 'select',
      required: false,
      options: classrooms.map((c) => ({ value: c.id, label: c.number })),
    },
  ];

  return (
    <CrudPage
      title="Учителя"
      icon="👨‍🏫"
      service={teachersService}
      columns={columns}
      formFields={formFields}
      initialFormData={{ first_name: '', last_name: '', patronymic: '', classroom: '' }}
    />
  );
}

