import CrudPage from '../components/CrudPage';
import { classroomsService } from '../api/services';

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'number', label: 'Номер' },
  { key: 'classroom_type_display', label: 'Тип' },
  { key: 'description', label: 'Описание', render: (item) => item.description || '—' },
];

const formFields = [
  { name: 'number', label: 'Номер кабинета', type: 'text', required: true },
  {
    name: 'classroom_type',
    label: 'Тип кабинета',
    type: 'select',
    required: true,
    options: [
      { value: 'basic', label: 'Для базовых дисциплин' },
      { value: 'profile', label: 'Для профильных дисциплин' },
    ],
  },
  { name: 'description', label: 'Описание', type: 'textarea', required: false },
];

export default function Classrooms() {
  return (
    <CrudPage
      title="Кабинеты"
      icon="🚪"
      service={classroomsService}
      columns={columns}
      formFields={formFields}
      initialFormData={{ number: '', classroom_type: 'basic', description: '' }}
    />
  );
}

