import api from './auth'

export default {
  getClassPerformanceReport(classId, format = 'json') {
    return api.get('/api/reports/', {
      params: {
        type: 'class_performance',
        class_id: classId,
        format: format
      }
    })
  },

  getGenderStatistics() {
    return api.get('/api/reports/', {
      params: {
        type: 'gender_statistics'
      }
    })
  },

  getClassroomStatistics() {
    return api.get('/api/reports/', {
      params: {
        type: 'classroom_statistics'
      }
    })
  },

  downloadPdf(url) {
    return api.get(url, {
      responseType: 'blob'
    })
  },

  getTeachersBySubject() {
    return api.get('/api/subjects/teachers_count/')
  },

  exportReportToPdf(classId) {
    return api.get(`/api/reports/?type=class_performance&class_id=${classId}&format=pdf`, {
      responseType: 'blob'
    })
  }
}