import api from './axios';

// Generic CRUD factory
const createCrudService = (endpoint) => ({
  getAll: async (params = {}) => {
    const response = await api.get(`/${endpoint}/`, { params });
    return response.data;
  },
  getById: async (id) => {
    const response = await api.get(`/${endpoint}/${id}/`);
    return response.data;
  },
  create: async (data) => {
    const response = await api.post(`/${endpoint}/`, data);
    return response.data;
  },
  update: async (id, data) => {
    const response = await api.put(`/${endpoint}/${id}/`, data);
    return response.data;
  },
  patch: async (id, data) => {
    const response = await api.patch(`/${endpoint}/${id}/`, data);
    return response.data;
  },
  delete: async (id) => {
    await api.delete(`/${endpoint}/${id}/`);
  },
});

// Subjects
export const subjectsService = {
  ...createCrudService('subjects'),
  getTeacherCount: async () => {
    const response = await api.get('/subjects/teacher_count/');
    return response.data;
  },
};

// Classrooms
export const classroomsService = {
  ...createCrudService('classrooms'),
  getTypeCount: async () => {
    const response = await api.get('/classrooms/type_count/');
    return response.data;
  },
};

// Teachers
export const teachersService = {
  ...createCrudService('teachers'),
  getSameSubjectsAsInformaticsTeacher: async (classId) => {
    const response = await api.get('/teachers/same_subjects_as_informatics_teacher/', {
      params: { class_id: classId },
    });
    return response.data;
  },
};

// Teacher Subjects
export const teacherSubjectsService = createCrudService('teacher-subjects');

// School Classes
export const schoolClassesService = {
  ...createCrudService('classes'),
  getGenderStats: async () => {
    const response = await api.get('/classes/gender_stats/');
    return response.data;
  },
  getPerformanceReport: async (classId, quarterId) => {
    const response = await api.get(`/classes/${classId}/performance_report/`, {
      params: quarterId ? { quarter_id: quarterId } : {},
    });
    return response.data;
  },
};

// Students
export const studentsService = {
  ...createCrudService('students'),
  getByClass: async (classId) => {
    const response = await api.get('/students/', {
      params: { school_class: classId },
    });
    return response.data;
  },
};

// Quarters
export const quartersService = {
  ...createCrudService('quarters'),
  getCurrent: async () => {
    const response = await api.get('/quarters/current/');
    return response.data;
  },
};

// Teaching Assignments
export const teachingAssignmentsService = {
  ...createCrudService('teaching-assignments'),
  getFiltered: async (teacherId, classId, quarterId) => {
    const params = {};
    if (teacherId) params.teacher = teacherId;
    if (classId) params.school_class = classId;
    if (quarterId) params.quarter = quarterId;
    const response = await api.get('/teaching-assignments/', { params });
    return response.data;
  },
};

// Schedule
export const scheduleService = {
  ...createCrudService('schedule'),
  getByClassDayLesson: async (classId, dayOfWeek, lessonNumber) => {
    const response = await api.get('/schedule/by_class_day_lesson/', {
      params: {
        school_class: classId,
        day_of_week: dayOfWeek,
        lesson_number: lessonNumber,
      },
    });
    return response.data;
  },
  getFiltered: async (classId, dayOfWeek, lessonNumber) => {
    const params = {};
    if (classId) params.school_class = classId;
    if (dayOfWeek) params.day_of_week = dayOfWeek;
    if (lessonNumber) params.lesson_number = lessonNumber;
    const response = await api.get('/schedule/', { params });
    return response.data;
  },
};

// Grades
export const gradesService = {
  ...createCrudService('grades'),
  getFiltered: async (studentId, subjectId, quarterId, classId) => {
    const params = {};
    if (studentId) params.student = studentId;
    if (subjectId) params.subject = subjectId;
    if (quarterId) params.quarter = quarterId;
    if (classId) params.school_class = classId;
    const response = await api.get('/grades/', { params });
    return response.data;
  },
};

