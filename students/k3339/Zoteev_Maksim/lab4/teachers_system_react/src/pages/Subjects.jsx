import CrudPage from '../components/CrudPage';
import { subjectsService } from '../api/services';

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'name', label: 'Название' },
  { key: 'subject_type_display', label: 'Тип' },
];

const formFields = [
  { name: 'name', label: 'Название', type: 'text', required: true },
  {
    name: 'subject_type',
    label: 'Тип предмета',
    type: 'select',
    required: true,
    options: [
      { value: 'basic', label: 'Базовый' },
      { value: 'profile', label: 'Профильный' },
    ],
  },
];

export default function Subjects() {
  return (
    <CrudPage
      title="Предметы"
      icon="📚"
      service={subjectsService}
      columns={columns}
      formFields={formFields}
      initialFormData={{ name: '', subject_type: 'basic' }}
    />
  );
}

