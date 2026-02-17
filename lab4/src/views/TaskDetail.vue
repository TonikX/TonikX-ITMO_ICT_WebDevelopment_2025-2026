<template>
  <div class="task-detail-page">
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else-if="task" class="task-detail">
      <div class="task-header">
        <h1>{{ task.title }}</h1>
        <router-link to="/tasks" class="btn btn-secondary">← Назад к списку</router-link>
      </div>

      <div class="task-content">
        <div class="task-section">
          <h2>Описание</h2>
          <p class="task-description">{{ task.description }}</p>
        </div>

        <div class="task-section">
          <h2>Информация</h2>
          <div class="task-info">
            <p><strong>Создатель:</strong> {{ task.created_by_username }}</p>
            <p v-if="task.curator_username"><strong>Куратор:</strong> {{ task.curator_username }}</p>
            <p v-if="task.consultation_link">
              <strong>Консультация:</strong>
              <a :href="task.consultation_link" target="_blank">{{ task.consultation_link }}</a>
            </p>
            <p><strong>Команд выбрало задачу:</strong> {{ task.teams_count || 0 }}</p>
            <p><strong>Создано:</strong> {{ formatDate(task.created_at) }}</p>
          </div>
        </div>

        <div v-if="isCurator && task.id" class="task-section">
          <h2>Управление задачей</h2>
          <div class="curator-actions">
            <div class="curator-form">
              <h3>Добавить файл</h3>
              <form @submit.prevent="handleAddFile">
                <input
                  ref="fileInput"
                  type="file"
                  @change="handleFileChange"
                  class="input"
                />
                <input
                  v-model="fileData.name"
                  type="text"
                  placeholder="Название файла"
                  class="input"
                  required
                />
                <button type="submit" class="btn" :disabled="loading">Добавить файл</button>
              </form>
            </div>

            <div class="curator-form">
              <h3>Добавить ссылку</h3>
              <form @submit.prevent="handleAddLink">
                <input
                  v-model="linkData.url"
                  type="url"
                  placeholder="URL"
                  class="input"
                  required
                />
                <input
                  v-model="linkData.title"
                  type="text"
                  placeholder="Название ссылки"
                  class="input"
                  required
                />
                <button type="submit" class="btn" :disabled="loading">Добавить ссылку</button>
              </form>
            </div>

            <div class="curator-form">
              <h3>Ссылка на консультацию</h3>
              <form @submit.prevent="handleSetConsultation">
                <input
                  v-model="consultationLink"
                  type="url"
                  placeholder="URL консультации"
                  class="input"
                />
                <button type="submit" class="btn" :disabled="loading">Сохранить</button>
              </form>
            </div>
          </div>
        </div>

        <div v-if="task.files && task.files.length > 0" class="task-section">
          <h2>Файлы</h2>
          <ul class="files-list">
            <li v-for="file in task.files" :key="file.id" class="file-item">
              <a :href="file.file_url" target="_blank">{{ file.name }}</a>
              <span class="file-date">{{ formatDate(file.uploaded_at) }}</span>
            </li>
          </ul>
        </div>

        <div v-if="task.links && task.links.length > 0" class="task-section">
          <h2>Ссылки</h2>
          <ul class="links-list">
            <li v-for="link in task.links" :key="link.id" class="link-item">
              <a :href="link.url" target="_blank">{{ link.title }}</a>
              <span class="link-date">{{ formatDate(link.created_at) }}</span>
            </li>
          </ul>
        </div>

        <div v-if="task.solutions && task.solutions.length > 0" class="task-section">
          <h2>Решения</h2>
          <div class="solutions-list">
            <div v-for="solution in task.solutions" :key="solution.id" class="solution-item">
              <h3>{{ solution.team_name }}</h3>
              <p>{{ solution.description }}</p>
              <router-link :to="`/solutions/${solution.id}`" class="btn">Подробнее</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { tasksAPI, apiErrorMessage } from '@/api'

export default {
  name: 'TaskDetail',
  data() {
    return {
      task: null,
      loading: false,
      error: '',
      fileData: {
        name: ''
      },
      selectedFile: null,
      linkData: {
        url: '',
        title: ''
      },
      consultationLink: ''
    }
  },
  computed: {
    isCurator() {
      if (!this.task) return false
      const userStr = localStorage.getItem('user')
      const user = userStr ? JSON.parse(userStr) : null
      return user?.role === 'curator' && this.task?.curator === user.id
    }
  },
  mounted() {
    this.loadTask()
  },
  methods: {
    async loadTask() {
      this.loading = true
      this.error = ''
      try {
        this.task = await tasksAPI.getDetail(this.$route.params.id)
        this.consultationLink = this.task.consultation_link || ''
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    handleFileChange(event) {
      this.selectedFile = event.target.files[0]
    },
    async handleAddFile() {
      if (!this.selectedFile) {
        this.error = 'Выберите файл'
        return
      }
      this.loading = true
      this.error = ''
      try {
        const formData = new FormData()
        formData.append('file', this.selectedFile)
        formData.append('name', this.fileData.name)
        await tasksAPI.addFile(this.task.id, formData)
        this.fileData = { name: '' }
        this.selectedFile = null
        this.$refs.fileInput.value = ''
        await this.loadTask()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async handleAddLink() {
      this.loading = true
      this.error = ''
      try {
        await tasksAPI.addLink(this.task.id, this.linkData)
        this.linkData = { url: '', title: '' }
        await this.loadTask()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async handleSetConsultation() {
      this.loading = true
      this.error = ''
      try {
        await tasksAPI.setConsultationLink(this.task.id, this.consultationLink)
        await this.loadTask()
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU')
    }
  }
}
</script>

<style scoped>
.task-detail-page {
  max-width: 1000px;
  margin: 0 auto;
}

.task-detail {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.task-header h1 {
  margin: 0;
  color: #2d7ef7;
}

.task-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.task-section h2 {
  margin: 0 0 1rem 0;
  color: #2d7ef7;
  font-size: 1.25rem;
}

.task-description {
  line-height: 1.6;
  color: #333;
}

.task-info p {
  margin: 0.5rem 0;
  color: #666;
}

.task-info a {
  color: #2d7ef7;
  text-decoration: none;
}

.task-info a:hover {
  text-decoration: underline;
}

.curator-actions {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.curator-form {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.curator-form h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
  color: #2d7ef7;
}

.files-list,
.links-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.file-item,
.link-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.file-item a,
.link-item a {
  color: #2d7ef7;
  text-decoration: none;
}

.file-item a:hover,
.link-item a:hover {
  text-decoration: underline;
}

.file-date,
.link-date {
  font-size: 0.9rem;
  color: #888;
}

.solutions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.solution-item {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.solution-item h3 {
  margin: 0 0 0.5rem 0;
  color: #2d7ef7;
}

.solution-item p {
  margin: 0 0 0.75rem 0;
  color: #666;
}

.loading,
.error-message {
  text-align: center;
  padding: 2rem;
}

.error-message {
  background: #fee;
  color: #c33;
  border-radius: 4px;
}
</style>
