import api from './auth'

export default {
  getClassPerformanceReport(classId, quarter = 1, schoolYear = '2025-2026') {
    return api.get('/api/reports/class_performance_report/', {
      params: {
        class_id: classId,
        quarter,
        school_year: schoolYear
      }
    })
  },

  getGenderStatistics() {
    return api.get('/api/reports/gender_count_per_class/').then(response => {
      const data = response.data || {}
      const mapped = Object.entries(data).map(([className, counts]) => ({
        class_name: className,
        boys_count: counts.M || 0,
        girls_count: counts.F || 0,
        total_students: (counts.M || 0) + (counts.F || 0)
      }))
      response.data = mapped
      return response
    })
  },

  getClassroomStatistics() {
    return api.get('/api/reports/classroom_stats/').then(response => {
      const data = Array.isArray(response.data) ? response.data : []
      response.data = data.map(item => ({
        subject_type: item.subject_type,
        subject_type_display: item.subject_type === 'profile' ? 'Профильные' : 'Базовые',
        classroom_count: item.count
      }))
      return response
    })
  },

  downloadPdf(url) {
    return api.get(url, {
      responseType: 'blob'
    })
  },

  getTeachersBySubject() {
    return api.get('/api/reports/teachers_per_subject/').then(response => {
      const data = Array.isArray(response.data) ? response.data : []
      response.data = data.map(item => ({
        subject: item.subject__name,
        teachers_count: item.teacher_count
      }))
      return response
    })
  },

  exportReportToPdf(classId, quarter = 1, schoolYear = '2025-2026') {
    return api.get('/api/reports/class_performance_report/', {
      params: {
        class_id: classId,
        quarter,
        school_year: schoolYear
      }
    })
  }
}