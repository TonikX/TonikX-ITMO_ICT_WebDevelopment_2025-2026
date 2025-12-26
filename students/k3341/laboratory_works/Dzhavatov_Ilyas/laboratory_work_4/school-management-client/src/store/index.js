import { createStore } from 'vuex'
import auth from './modules/auth'
import teachers from './modules/teachers'
import students from './modules/students'

export default createStore({
  state: {
    loading: false,
    error: null
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_ERROR(state) {
      state.error = null
    }
  },
  actions: {
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading)
    },
    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    clearError({ commit }) {
      commit('CLEAR_ERROR')
    }
  },
  getters: {
    isLoading: state => state.loading,
    error: state => state.error
  },
  modules: {
    auth,
    teachers,
    students
  }
})