<template>
  <div class="admin-reader-register">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card>
            <v-card-title class="text-h5">
              <v-icon left color="primary">mdi-account-plus</v-icon>
              Регистрация читателя
            </v-card-title>

            <v-card-text>
              <v-form ref="formRef" v-model="valid">
                <v-row>
                  <v-col cols="12"><h4 class="text-subtitle-2 mb-2">📋 Основные данные</h4></v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="form.full_name" :rules="[v => !!v]" label="ФИО *" placeholder="Иванов Иван Иванович"
                      density="comfortable" variant="outlined" required />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="form.passport" :rules="[v => !!v]" label="Паспорт *" placeholder="1234 567890"
                      density="comfortable" variant="outlined" required />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="form.birth_date" :rules="[v => !!v]" label="Дата рождения *" type="date"
                      density="comfortable" variant="outlined" required />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select v-model="form.education_level" :items="levels" :rules="[v => !!v]" label="Образование *"
                      density="comfortable" variant="outlined" required />
                  </v-col>

                  <v-col cols="12"><v-divider class="my-2" /><h4 class="text-subtitle-2 mb-2">📞 Контакты</h4></v-col>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="form.phone_number" :rules="[v => !!v]" label="Телефон *" placeholder="+7 (999) 123-45-67"
                      density="comfortable" variant="outlined" required />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select v-model="form.hall_id" :items="halls" :rules="[v => !!v]" item-title="name" item-value="hall_id"
                      label="Зал *" density="comfortable" variant="outlined" required />
                  </v-col>
                  <v-col cols="12">
                    <v-textarea v-model="form.home_address" :rules="[v => !!v]" label="Адрес *" rows="2"
                      placeholder="г. Москва, ул. Пушкина, д. 10, кв. 5" density="comfortable" variant="outlined" required />
                  </v-col>
                </v-row>
              </v-form>

              <v-alert v-if="error" type="error" class="mt-3" closable @click:close="error = ''">{{ error }}</v-alert>
              <v-alert v-if="success" type="success" class="mt-3">
                ✅ Читатель зарегистрирован<br><small>Билет: {{ newReader?.library_card_id }}</small>
              </v-alert>
            </v-card-text>

            <v-card-actions class="pa-4">
              <v-spacer />
              <v-btn color="grey" variant="text" @click="$router.push('/admin/readers')">Отмена</v-btn>
              <v-btn color="primary" :loading="loading" @click="register">Зарегистрировать</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/client'

const router = useRouter()
const formRef = ref(null)
const valid = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref(false)
const newReader = ref(null)
const halls = ref([])

const form = reactive({
  full_name: '', passport: '', birth_date: '', education_level: '',
  phone_number: '', home_address: '', hall_id: null
})

const levels = [
  { title: 'Начальное', value: 'primary' },
  { title: 'Среднее', value: 'secondary' },
  { title: 'Высшее', value: 'higher' },
  { title: 'Ученая степень', value: 'degree' }
]

const loadHalls = async () => {
  try { halls.value = (await apiClient.get('halls/')).data }
  catch (e) { console.error('Ошибка загрузки залов:', e) }
}

const register = async () => {
  if (!formRef.value?.validate()) return
  loading.value = true; error.value = ''; success.value = false
  try {
    const res = await apiClient.post('reader/register/', form)
    newReader.value = res.data
    success.value = true
    Object.keys(form).forEach(k => form[k] = k === 'hall_id' ? null : '')
    setTimeout(() => router.push('/admin/readers'), 2000)
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка регистрации'
  } finally { loading.value = false }
}

onMounted(loadHalls)
</script>

<style scoped>
.admin-reader-register { width: 100%; min-height: 100%; }
.v-card { border-radius: 12px; }
.v-card-title { background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%); border-bottom: 1px solid #ddd; }
.register-container { max-width: 1200px; margin: 0 auto; }
</style>