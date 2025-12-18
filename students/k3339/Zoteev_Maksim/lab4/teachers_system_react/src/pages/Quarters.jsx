import CrudPage from '../components/CrudPage';
import { quartersService } from '../api/services';

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'number_display', label: 'Четверть' },
  { key: 'academic_year', label: 'Учебный год' },
  { key: 'start_date', label: 'Начало' },
  { key: 'end_date', label: 'Конец' },
  {
    key: 'is_current',
    label: 'Текущая',
    render: (item) => (item.is_current ? '✅' : '—'),
  },
];

const formFields = [
  {
    name: 'number',
    label: 'Номер четверти',
    type: 'select',
    required: true,
    options: [
      { value: 1, label: 'I четверть' },
      { value: 2, label: 'II четверть' },
      { value: 3, label: 'III четверть' },
      { value: 4, label: 'IV четверть' },
    ],
  },
  { name: 'academic_year', label: 'Учебный год (напр. 2024-2025)', type: 'text', required: true },
  { name: 'start_date', label: 'Дата начала', type: 'date', required: true },
  { name: 'end_date', label: 'Дата окончания', type: 'date', required: true },
  { name: 'is_current', label: 'Текущая четверть', type: 'checkbox', required: false },
];

export default function Quarters() {
  return (
    <CrudPage
      title="Четверти"
      icon="📅"
      service={quartersService}
      columns={columns}
      formFields={formFields}
      initialFormData={{
        number: 1,
        academic_year: '',
        start_date: '',
        end_date: '',
        is_current: false,
      }}
    />
  );
}

