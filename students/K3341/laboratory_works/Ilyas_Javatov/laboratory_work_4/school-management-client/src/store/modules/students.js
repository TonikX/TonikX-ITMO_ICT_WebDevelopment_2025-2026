const state = {
  students: [],
  currentStudent: null,
  loading: false,
  error: null
}

const getters = {
  allStudents: state => state.students,
  currentStudent: state => state.currentStudent,
  isLoading: state => state.loading,
  error: state => state.error
}

const mutations = {
  SET_STUDENTS(state, students) {
    state.students = students
  },
  SET_CURRENT_STUDENT(state, student) {
    state.currentStudent = student
  },
  ADD_STUDENT(state, student) {
    state.students.push(student)
  },
  UPDATE_STUDENT(state, updatedStudent) {
    const index = state.students.findIndex(s => s.id === updatedStudent.id)
    if (index !== -1) {
      state.students.splice(index, 1, updatedStudent)
    }
  },
  REMOVE_STUDENT(state, studentId) {
    state.students = state.students.filter(s => s.id !== studentId)
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
  CLEAR_ERROR(state) {
    state.error = null
  }
}

const actions = {
  async fetchStudents({ commit }) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // const response = await api.getStudents()
      // commit('SET_STUDENTS', response.data)
      commit('SET_LOADING', false)
    } catch (error) {
      commit('SET_ERROR', error.message)
      commit('SET_LOADING', false)
    }
  },

  async fetchStudent({ commit }, studentId) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // const response = await api.getStudent(studentId)
      // commit('SET_CURRENT_STUDENT', response.data)
      commit('SET_LOADING', false)
    } catch (error) {
      commit('SET_ERROR', error.message)
      commit('SET_LOADING', false)
    }
  },

  async createStudent({ commit }, studentData) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // const response = await api.createStudent(studentData)
      // commit('ADD_STUDENT', response.data)
      commit('SET_LOADING', false)
      return { success: true }
    } catch (error) {
      commit('SET_ERROR', error.message)
      commit('SET_LOADING', false)
      return { success: false, error: error.message }
    }
  },

  async updateStudent({ commit }, { studentId, studentData }) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // const response = await api.updateStudent(studentId, studentData)
      // commit('UPDATE_STUDENT', response.data)
      commit('SET_LOADING', false)
      return { success: true }
    } catch (error) {
      commit('SET_ERROR', error.message)
      commit('SET_LOADING', false)
      return { success: false, error: error.message }
    }
  },

  async deleteStudent({ commit }, studentId) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // await api.deleteStudent(studentId)
      commit('REMOVE_STUDENT', studentId)
      commit('SET_LOADING', false)
      return { success: true }
    } catch (error) {
      commit('SET_ERROR', error.message)
      commit('SET_LOADING', false)
      return { success: false, error: error.message }
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}