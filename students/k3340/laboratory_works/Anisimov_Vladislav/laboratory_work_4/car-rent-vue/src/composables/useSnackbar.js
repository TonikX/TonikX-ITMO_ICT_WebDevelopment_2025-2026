// composables/useSnackbar.js
import { ref } from 'vue'

export const useSnackbar = () => {
  const snackbar = ref({
    show: false,
    message: '',
    color: 'success',
    timeout: 3000,
    location: 'bottom right'
  })

  const showSnackbar = (message, color = 'success', timeout = 3000) => {
    snackbar.value = {
      show: true,
      message,
      color,
      timeout,
      location: 'bottom right'
    }
  }

  const showSuccess = (message) => {
    showSnackbar(message, 'success')
  }

  const showError = (message) => {
    showSnackbar(message, 'error')
  }

  const showWarning = (message) => {
    showSnackbar(message, 'warning')
  }

  const showInfo = (message) => {
    showSnackbar(message, 'info')
  }

  const hideSnackbar = () => {
    snackbar.value.show = false
  }

  return {
    snackbar,
    showSnackbar,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    hideSnackbar
  }
}