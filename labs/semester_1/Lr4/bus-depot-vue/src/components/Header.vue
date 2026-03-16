<template>
  <v-app-bar flat color="surface" app>
    <div class="d-flex align-center w-100 mx-auto" style="max-width: 1200px;">
      <v-app-bar-title>
        <router-link to="/main" class="text-decoration-none text-primary">
          Главная
        </router-link>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <div class="d-flex align-center">
        <router-link 
          to="/profile" 
          class="text-decoration-none text-body-1 mr-4"
        >
          {{ username }}
        </router-link>
        
        <v-btn
          variant="text"
          color="primary"
          @click="confirmLogout"
        >
          Выйти
        </v-btn>
      </div>
    </div>
  </v-app-bar>
</template>


<script>
import axios from 'axios'

export default {
    data() {
        return {
            username: localStorage.getItem("username"),
        }
    },
    methods: {
        confirmLogout() {
            if (confirm('Вы уверены, что хотите выйти?')) {
                this.handleLogout()
            }
        },

        async handleLogout() {
            try {
                const token = localStorage.getItem('auth_token')

                if (token) {
                    await axios.post('http://127.0.0.1:8000/auth/token/logout/', {}, {
                        headers: {
                            'Authorization': `Token ${token}`
                        }
                    })
                }

                this.clearAuthAndRedirect()
            } catch (error) {
                this.clearAuthAndRedirect()
            }
        },

        clearAuthAndRedirect() {
            localStorage.clear()
            this.$router.push('/auth')
        },

        updateUsername() {
            this.username = localStorage.getItem("username");
        }
    }
}
</script>
