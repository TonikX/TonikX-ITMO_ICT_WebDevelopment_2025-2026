const state = {
  teachers: [],
  currentTeacher: null,
  loading: false,
  error: null
}

const getters = {
  allTeachers: state => state.teachers,
  currentTeacher: state => state.currentTeacher,
  isLoading: state => state.loading,
  error: state => state.error
}

const mutations = {
  SET_TEACHERS(state, teachers) {
    state.teachers = teachers
  },
  SET_CURRENT_TEACHER(state, teacher) {
    state.currentTeacher = teacher
  },
  ADD_TEACHER(state, teacher) {
    state.teachers.push(teacher)
  },
  UPDATE_TEACHER(state, updatedTeacher) {
    const index = state.teachers.findIndex(t => t.id === updatedTeacher.id)
    if (index !== -1) {
      state.teachers.splice(index, 1, updatedTeacher)
    }
  },
  REMOVE_TEACHER(state, teacherId) {
    state.teachers = state.teachers.filter(t => t.id !== teacherId)
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
  async fetchTeachers({ commit }) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // const response = await api.getTeachers()
      // commit('SET_TEACHERS', response.data)
      commit('SET_LOADING', false)
    } catch (error) {
      commit('SET_ERROR', error.message)
      commit('SET_LOADING', false)
    }
  },

  async fetchTeacher({ commit }, teacherId) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // const response = await api.getTeacher(teacherId)
      // commit('SET_CURRENT_TEACHER', response.data)
      commit('SET_LOADING', false)
    } catch (error) {
      commit('SET_ERROR', error.message)
      commit('SET_LOADING', false)
    }
  },

  async createTeacher({ commit }, teacherData) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // const response = await api.createTeacher(teacherData)
      // commit('ADD_TEACHER', response.data)
      commit('SET_LOADING', false)
      return { success: true }
    } catch (error) {
      commit('SET_ERROR', error.message)
      commit('SET_LOADING', false)
      return { success: false, error: error.message }
    }
  },

  async updateTeacher({ commit }, { teacherId, teacherData }) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // const response = await api.updateTeacher(teacherId, teacherData)
      // commit('UPDATE_TEACHER', response.data)
      commit('SET_LOADING', false)
      return { success: true }
    } catch (error) {
      commit('SET_ERROR', error.message)
      commit('SET_LOADING', false)
      return { success: false, error: error.message }
    }
  },

  async deleteTeacher({ commit }, teacherId) {
    commit('SET_LOADING', true)
    commit('CLEAR_ERROR')
    try {
      // Здесь будет API запрос
      // await api.deleteTeacher(teacherId)
      commit('REMOVE_TEACHER', teacherId)
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