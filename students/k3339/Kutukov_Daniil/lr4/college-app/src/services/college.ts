import api from './api'

export interface Group {
    id: number
    name: string
    course: number
    specialty: string
}

export interface Student {
    id: number
    first_name: string
    last_name: string
    middle_name: string
    group: number | Group
    enrollment_date: string
    phone: string
    email: string
}

export interface Teacher {
    id: number
    first_name: string
    last_name: string
    middle_name: string
    subjects: number[]
    classroom: number | null
    phone: string
    email: string
}

export interface Subject {
    id: number
    name: string
    hours_per_semester: number
}

export interface Grade {
    id: number
    student: number
    subject: number
    grade: number
    semester: number
    date: string
}

export interface Schedule {
    id: number
    group: number
    subject: number
    teacher: number
    classroom: number
    day_of_week: number
    lesson_number: number
    start_time: string
    end_time: string
}

export const collegeService = {
    // Groups
    async getGroups() {
        const response = await api.get<Group[]>('/groups/')
        return response.data
    },

    async getGroup(id: number) {
        const response = await api.get(`/groups/${id}/`)
        return response.data
    },

    async getGroupTeachers(id: number) {
        const response = await api.get(`/groups/${id}/teachers/`)
        return response.data
    },

    async getGradeSheet(groupId: number, semester: number) {
        const response = await api.get(`/groups/${groupId}/grade_sheet/`, {
            params: { semester }
        })
        return response.data
    },

    async getStudentsPerCourse() {
        const response = await api.get('/groups/students_per_course/')
        return response.data
    },

    // Students
    async getStudents() {
        const response = await api.get<Student[]>('/students/')
        return response.data
    },

    async getStudent(id: number) {
        const response = await api.get(`/students/${id}/`)
        return response.data
    },

    async getStudentGrades(id: number, semester?: number) {
        const params = semester ? { semester } : {}
        const response = await api.get(`/students/${id}/grades/`, { params })
        return response.data
    },

    async createStudent(data: Partial<Student>) {
        const response = await api.post('/students/', data)
        return response.data
    },

    async updateStudent(id: number, data: Partial<Student>) {
        const response = await api.patch(`/students/${id}/`, data)
        return response.data
    },

    async deleteStudent(id: number) {
        await api.delete(`/students/${id}/`)
    },

    // Teachers
    async getTeachers() {
        const response = await api.get<Teacher[]>('/teachers/')
        return response.data
    },

    async getTeacher(id: number) {
        const response = await api.get(`/teachers/${id}/`)
        return response.data
    },

    async createTeacher(data: Partial<Teacher>) {
        const response = await api.post('/teachers/', data)
        return response.data
    },

    async updateTeacher(id: number, data: Partial<Teacher>) {
        const response = await api.patch(`/teachers/${id}/`, data)
        return response.data
    },

    async deleteTeacher(id: number) {
        await api.delete(`/teachers/${id}/`)
    },

    async getTeacherSubjectGroups(teacherId: number, subjectId: number) {
        const response = await api.get(`/teachers/${teacherId}/subject_groups/`, {
            params: { subject: subjectId }
        })
        return response.data
    },

    // Subjects
    async getSubjects() {
        const response = await api.get<Subject[]>('/subjects/')
        return response.data
    },

    async createSubject(data: Partial<Subject>) {
        const response = await api.post('/subjects/', data)
        return response.data
    },

    async updateSubject(id: number, data: Partial<Subject>) {
        const response = await api.patch(`/subjects/${id}/`, data)
        return response.data
    },

    async deleteSubject(id: number) {
        await api.delete(`/subjects/${id}/`)
    },

    // Schedules
    async getSchedules() {
        const response = await api.get<Schedule[]>('/schedules/')
        return response.data
    },

    async createSchedule(data: Partial<Schedule>) {
        const response = await api.post('/schedules/', data)
        return response.data
    },

    async updateSchedule(id: number, data: Partial<Schedule>) {
        const response = await api.patch(`/schedules/${id}/`, data)
        return response.data
    },

    async deleteSchedule(id: number) {
        await api.delete(`/schedules/${id}/`)
    },

    async getGroupDaySchedule(groupId: number, day: number) {
        const response = await api.get('/schedules/group_day_schedule/', {
            params: { group: groupId, day }
        })
        return response.data
    },

    async getLessonInfo(groupId: number, day: number, lesson: number) {
        const response = await api.get('/schedules/lesson_info/', {
            params: { group: groupId, day, lesson }
        })
        return response.data
    },

    // Grades
    async getGrades() {
        const response = await api.get<Grade[]>('/grades/')
        return response.data
    },

    async createGrade(data: Partial<Grade>) {
        const response = await api.post('/grades/', data)
        return response.data
    },

    async updateGrade(id: number, data: Partial<Grade>) {
        const response = await api.put(`/grades/${id}/`, data)
        return response.data
    },

    async deleteGrade(id: number) {
        await api.delete(`/grades/${id}/`)
    },

    // Groups
    async createGroup(data: Partial<Group>) {
        const response = await api.post('/groups/', data)
        return response.data
    },

    async updateGroup(id: number, data: Partial<Group>) {
        const response = await api.patch(`/groups/${id}/`, data)
        return response.data
    },

    async deleteGroup(id: number) {
        await api.delete(`/groups/${id}/`)
    },

    // Classrooms
    async getClassrooms() {
        const response = await api.get<any[]>('/classrooms/')
        return response.data
    },
}
