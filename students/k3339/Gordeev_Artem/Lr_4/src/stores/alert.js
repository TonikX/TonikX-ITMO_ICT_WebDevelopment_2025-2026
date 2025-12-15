import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAlertStore = defineStore('alert', () => {
    const visible = ref(false)
    const message = ref('')
    const type = ref('info') // 'success' (успех), 'info' (инфо), 'warning' (предупреждение), 'error' (ошибка)
    const timeout = ref(3000)

    const show = (msg, msgType = 'info', duration = 3000) => {
        message.value = msg
        type.value = msgType
        timeout.value = duration
        visible.value = true
    }

    const showError = (err) => {
        let msg = 'Произошла ошибка'
        if (err.response) {
            if (err.response.data) {
                if (typeof err.response.data === 'object') {
                    // Если это массив (как в non_field_errors) или объект полей
                    msg = Object.entries(err.response.data)
                        .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(', ') : val}`)
                        .join('; ')
                } else {
                    msg = String(err.response.data)
                }
            } else {
                msg = `Ошибка ${err.response.status}: ${err.response.statusText}`
            }
        } else if (err.message) {
            msg = err.message
        }
        show(msg, 'error')
    }

    const close = () => {
        visible.value = false
    }

    return { visible, message, type, timeout, show, showError, close }
})
