<template>
<div>
    Проверка авторизации...
</div>
</template>

<script>
import axios from 'axios'

export default {
    async mounted() {
        const token = localStorage.getItem('auth_token')

        if (!token) {
            this.$router.push('/auth')
            return
        }

        try {
            const response = await axios.get('http://127.0.0.1:8000/auth/users/me/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            })

            if (response.status === 200) {
                this.$router.push('/main')
            } else {
                this.$router.push('/auth')
            }
        } catch (error) {
            this.$router.push('/auth')
        }
    }
}
</script>
