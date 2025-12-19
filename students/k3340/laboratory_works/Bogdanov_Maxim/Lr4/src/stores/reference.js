import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/client'

export const useReferenceStore = defineStore('reference', () => {
  const classes = ref([])
  const teachers = ref([])
  const students = ref([])
  const subjects = ref([])
  const classrooms = ref([])
  const academicYears = ref([])
  const gradingPeriods = ref([])
  const weekdays = ref([])

  const loadClasses = async () => {
    try {
      const response = await api.get('/classes')
      classes.value = response.data || []
    } catch (error) {
      console.error('Ошибка загрузки классов:', error)
    }
  }

  const loadTeachers = async () => {
    try {
      const response = await api.get('/teachers')
      teachers.value = response.data || []
    } catch (error) {
      console.error('Ошибка загрузки учителей:', error)
    }
  }

  const loadStudents = async () => {
    try {
      const response = await api.get('/students')
      students.value = response.data || []
    } catch (error) {
      console.error('Ошибка загрузки учеников:', error)
    }
  }

  const getClassLabel = (classId) => {
    const classItem = classes.value.find(c => c.id === classId)
    if (!classItem) return `ID: ${classId}`
    return `${classItem.grade}${classItem.letter}`
  }

  const getTeacherLabel = (teacherId) => {
    const teacher = teachers.value.find(t => t.id === teacherId)
    if (!teacher) return `ID: ${teacherId}`
    return `${teacher.last_name} ${teacher.first_name} ${teacher.middle_name || ''}`.trim()
  }

  const getStudentLabel = (studentId) => {
    const student = students.value.find(s => s.id === studentId)
    if (!student) return `ID: ${studentId}`
    return `${student.last_name} ${student.first_name} ${student.middle_name || ''}`.trim()
  }

  const getClassroomLabel = (classroomId) => {
    const classroom = classrooms.value.find(c => c.id === classroomId)
    if (!classroom) return `ID: ${classroomId}`
    return `Кабинет ${classroom.room_number}`
  }

  const getSubjectLabel = (subjectId) => {
    const subject = subjects.value.find(s => s.id === subjectId)
    if (!subject) return `ID: ${subjectId}`
    return subject.name
  }

  const getGradingPeriodLabel = (periodId) => {
    const period = gradingPeriods.value.find(p => p.id === periodId)
    if (!period) return `ID: ${periodId}`
    return period.name
  }

  const getWeekdayLabel = (weekdayId) => {
    const weekday = weekdays.value.find(w => w.id === weekdayId)
    if (!weekday) return `ID: ${weekdayId}`
    return weekday.name
  }

  // Загрузка всех справочных данных
  const loadSubjects = async () => {
    try {
      const response = await api.get('/reference/subjects')
      subjects.value = response.data || []
    } catch (error) {
      console.error('Ошибка загрузки предметов:', error)
    }
  }

  const loadClassrooms = async () => {
    try {
      const response = await api.get('/reference/classrooms')
      classrooms.value = response.data || []
    } catch (error) {
      console.error('Ошибка загрузки кабинетов:', error)
    }
  }

  const loadAcademicYears = async () => {
    try {
      const response = await api.get('/reference/academic-years')
      academicYears.value = response.data || []
    } catch (error) {
      console.error('Ошибка загрузки учебных годов:', error)
    }
  }

  const loadGradingPeriods = async () => {
    try {
      const response = await api.get('/reference/grading-periods')
      gradingPeriods.value = response.data || []
    } catch (error) {
      console.error('Ошибка загрузки периодов оценивания:', error)
    }
  }

  const loadWeekdays = async () => {
    try {
      const response = await api.get('/reference/weekdays')
      weekdays.value = response.data || []
    } catch (error) {
      console.error('Ошибка загрузки дней недели:', error)
    }
  }

  const loadAll = async () => {
    await Promise.all([
      loadClasses(),
      loadTeachers(),
      loadStudents(),
      loadSubjects(),
      loadClassrooms(),
      loadAcademicYears(),
      loadGradingPeriods(),
      loadWeekdays()
    ])
  }

  return {
    classes,
    teachers,
    students,
    subjects,
    classrooms,
    academicYears,
    gradingPeriods,
    weekdays,
    loadClasses,
    loadTeachers,
    loadStudents,
    loadSubjects,
    loadClassrooms,
    loadAcademicYears,
    loadGradingPeriods,
    loadWeekdays,
    loadAll,
    getClassLabel,
    getTeacherLabel,
    getStudentLabel,
    getClassroomLabel,
    getSubjectLabel,
    getGradingPeriodLabel,
    getWeekdayLabel
  }
})

