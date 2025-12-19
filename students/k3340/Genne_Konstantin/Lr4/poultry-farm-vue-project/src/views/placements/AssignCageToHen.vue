<template>
  <v-container>
    <v-card>
      <v-card-title>Поселить курицу в клетку</v-card-title>
      <v-form @submit.prevent="submit">
        <v-select
          v-model.number="form.hen"
          :items="hens"
          item-title="label"
          item-value="id"
          label="Курица *"
          :rules="[rules.required]"
          required
        />
        <v-select
          v-model.number="form.cage"
          :items="cages"
          item-title="label"
          item-value="id"
          label="Клетка *"
          :rules="[rules.required]"
          required
        />
        <v-text-field
          :value="formatDate(today)"
          label="Дата заселения"
          readonly
          variant="solo-filled"
        />
        <v-card-actions class="mt-4">
          <v-btn 
            type="submit" 
            color="primary" 
            :disabled="!isFormValid || loading"
            :loading="loading"
          >
            Поселить
          </v-btn>
          <v-btn to="/">Отмена</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getHens } from '@/api/hens'
import { getCages } from '@/api/cages'
import { getHenCages } from '@/api/henCages'
import { createHenCage, updateHenCage } from '@/api/henCages'

const today = new Date().toISOString().split('T')[0]
const yesterday = new Date()
yesterday.setDate(yesterday.getDate() - 1)
const yesterdayStr = yesterday.toISOString().split('T')[0]

const form = ref({
  hen: null,
  cage: null
})

const rules = {
  required: value => !!value || 'Обязательное поле'
}

const hens = ref([])
const cages = ref([])
const loading = ref(false)

const isFormValid = computed(() => {
  return form.value.hen !== null && form.value.cage !== null
})

onMounted(async () => {
  try {
    const hensRaw = await getHens()
    hens.value = hensRaw.map(h => ({
      id: h.id,
      label: `Курица #${h.id} — ${h.breed.name}, ${h.weight} г`
    }))

    const cagesRaw = await getCages()
    cages.value = cagesRaw.map(c => ({
      id: c.id,
      label: `Цех ${c.workshop_number}, ряд ${c.row_number}, клетка ${c.in_row_number}`
    }))
  } catch (err) {
    alert(err.response?.data?.error || 'Ошибка загрузки данных')
  }
})

const submit = async () => {
  if (!isFormValid.value) return

  loading.value = true
  const henId = form.value.hen
  const cageId = form.value.cage

  try {
    // Найти текущее заселение выбранной курицы
    const currentAssignments = await getHenCages({
      hen: henId,
      current_only: 'true'
    })

    // Выселить из предыдущей клетки (если есть)
    if (currentAssignments.length > 0) {
      await updateHenCage(currentAssignments[0].id, { 
        date_end: yesterdayStr 
      })
    }

    // Заселить в новую клетку
    await createHenCage({
      hen: henId,
      cage: cageId,
      date_start: today
    })

    // ✅ Успех: сброс формы + сообщение
    alert('Курица успешно поселена!')
    form.value = { hen: null, cage: null }

  } catch (err) {
    alert(err.response?.data?.error || 'Ошибка поселения')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr) => {
  return dateStr ? new Date(dateStr).toLocaleDateString('ru-RU') : ''
}
</script>