import { useState, useEffect } from 'react';
import CrudPage from '../components/CrudPage';
import {
  teachingAssignmentsService,
  teachersService,
  subjectsService,
  schoolClassesService,
  quartersService,
} from '../api/services';

export default function TeachingAssignments() {
  const [teachers, setTeachers] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [classes, setClasses] = useState([]);
  const [quarters, setQuarters] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [teachersData, subjectsData, classesData, quartersData] = await Promise.all([
          teachersService.getAll(),
          subjectsService.getAll(),
          schoolClassesService.getAll(),
          quartersService.getAll(),
        ]);
        setTeachers(teachersData.results || teachersData);
        setSubjects(subjectsData.results || subjectsData);
        setClasses(classesData.results || classesData);
        setQuarters(quartersData.results || quartersData);
      } catch (err) {
        console.error('Error loading data:', err);
      }
    };
    loadData();
  }, []);

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'teacher_name', label: 'Учитель' },
    { key: 'subject_name', label: 'Предмет' },
    { key: 'school_class_name', label: 'Класс' },
    { key: 'quarter_display', label: 'Четверть' },
  ];

  const formFields = [
    {
      name: 'teacher',
      label: 'Учитель',
      type: 'select',
      required: true,
      options: teachers.map((t) => ({ value: t.id, label: t.full_name })),
    },
    {
      name: 'subject',
      label: 'Предмет',
      type: 'select',
      required: true,
      options: subjects.map((s) => ({ value: s.id, label: s.name })),
    },
    {
      name: 'school_class',
      label: 'Класс',
      type: 'select',
      required: true,
      options: classes.map((c) => ({ value: c.id, label: c.name })),
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
  ];

  return (
    <CrudPage
      title="Назначения преподавания"
      icon="📝"
      service={teachingAssignmentsService}
      columns={columns}
      formFields={formFields}
      initialFormData={{ teacher: '', subject: '', school_class: '', quarter: '' }}
    />
  );
}

