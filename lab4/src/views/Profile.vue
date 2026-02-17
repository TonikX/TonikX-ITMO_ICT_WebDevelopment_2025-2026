<template>
  <div class="profile-page">
    <div class="page-header">
      <h1>Профиль</h1>
    </div>

    <div class="profile-card">
      <div v-if="loading" class="loading">Загрузка...</div>
      <form v-else @submit.prevent="handleSave">
        <div v-if="success" class="success-message">{{ success }}</div>
        <div v-if="error" class="error-message">{{ error }}</div>

        <div class="role-line">
          <strong>Роль:</strong> {{ roleLabel(form.role) }}
        </div>

        <input
          v-model.trim="form.username"
          type="text"
          placeholder="Имя пользователя"
          class="input"
          required
        />
        <input
          v-model.trim="form.email"
          type="email"
          placeholder="Email"
          class="input"
          required
        />
        <input
          v-model.trim="form.first_name"
          type="text"
          placeholder="Имя"
          class="input"
        />
        <input
          v-model.trim="form.last_name"
          type="text"
          placeholder="Фамилия"
          class="input"
        />

        <button type="submit" class="btn" :disabled="saving">
          {{ saving ? 'Сохранение...' : 'Сохранить изменения' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { authAPI, apiErrorMessage } from '@/api'

export default {
  name: 'Profile',
  data() {
    return {
      loading: true,
      saving: false,
      error: '',
      success: '',
      form: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: ''
      }
    }
  },
  async mounted() {
    await this.loadProfile()
  },
  methods: {
    async loadProfile() {
      this.loading = true
      this.error = ''
      try {
        const me = await authAPI.getMe()
        this.form = {
          username: me.username || '',
          email: me.email || '',
          first_name: me.first_name || '',
          last_name: me.last_name || '',
          role: me.role || ''
        }
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async handleSave() {
      this.saving = true
      this.error = ''
      this.success = ''
      try {
        const updated = await authAPI.updateMe({
          username: this.form.username,
          email: this.form.email,
          first_name: this.form.first_name,
          last_name: this.form.last_name
        })
        localStorage.setItem('user', JSON.stringify(updated))
        window.dispatchEvent(new Event('auth-changed'))
        this.success = 'Профиль обновлен'
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.saving = false
      }
    },
    roleLabel(role) {
      const labels = {
        admin: 'Администратор',
        captain: 'Капитан',
        curator: 'Куратор',
        jury: 'Жюри'
      }
      return labels[role] || role
    }
  }
}
</script>

<style scoped>
.profile-page {
  max-width: 760px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h1 {
  margin: 0;
  color: #2d7ef7;
}

.profile-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.role-line {
  margin-bottom: 1rem;
  color: #666;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.success-message {
  background: #e9f8ee;
  color: #1b7f3b;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}
</style>
