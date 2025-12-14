import { useState, useEffect } from 'react';
import CrudPage from '../components/CrudPage';
import {
  scheduleService,
  teachingAssignmentsService,
  classroomsService,
} from '../api/services';

const dayOptions = [
  { value: 1, label: 'Понедельник' },
  { value: 2, label: 'Вторник' },
  { value: 3, label: 'Среда' },
  { value: 4, label: 'Четверг' },
  { value: 5, label: 'Пятница' },
  { value: 6, label: 'Суббота' },
];

const lessonOptions = Array.from({ length: 8 }, (_, i) => ({
  value: i + 1,
  label: `${i + 1} урок`,
}));

export default function Schedule() {
  const [assignments, setAssignments] = useState([]);
  const [classrooms, setClassrooms] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [assignmentsData, classroomsData] = await Promise.all([
          teachingAssignmentsService.getAll(),
          classroomsService.getAll(),
        ]);
        setAssignments(assignmentsData.results || assignmentsData);
        setClassrooms(classroomsData.results || classroomsData);
      } catch (err) {
        console.error('Error loading data:', err);
      }
    };
    loadData();
  }, []);

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'day_of_week_display', label: 'День' },
    { key: 'lesson_number_display', label: 'Урок' },
    { key: 'subject_name', label: 'Предмет' },
    { key: 'teacher_name', label: 'Учитель' },
    { key: 'school_class_name', label: 'Класс' },
    { key: 'classroom_number', label: 'Кабинет', render: (item) => item.classroom_number || '—' },
  ];

  const formFields = [
    {
      name: 'teaching_assignment',
      label: 'Назначение',
      type: 'select',
      required: true,
      options: assignments.map((a) => ({
        value: a.id,
        label: `${a.teacher_name} - ${a.subject_name} (${a.school_class_name})`,
      })),
    },
    {
      name: 'day_of_week',
      label: 'День недели',
      type: 'select',
      required: true,
      options: dayOptions,
    },
    {
      name: 'lesson_number',
      label: 'Номер урока',
      type: 'select',
      required: true,
      options: lessonOptions,
    },
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
      title="Расписание"
      icon="🕐"
      service={scheduleService}
      columns={columns}
      formFields={formFields}
      initialFormData={{
        teaching_assignment: '',
        day_of_week: 1,
        lesson_number: 1,
        classroom: '',
      }}
    />
  );
}

