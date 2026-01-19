<template>
  <div class="d-flex flex-wrap" style="gap: 12px">
    <v-menu v-model="menu" :close-on-content-click="false">
      <template #activator="{ props: act }">
        <v-text-field
          v-bind="act"
          :label="label"
          :model-value="value.date"
          variant="outlined"
          density="compact"
          readonly
          :rules="dateRules"
        />
      </template>

      <v-card>
        <v-card-text>
          <v-date-picker
            :model-value="value.date || null"
            @update:model-value="onPickDate"
          >
            <template #header></template>
          </v-date-picker>
        </v-card-text>
      </v-card>
    </v-menu>

    <v-text-field
      label="Время"
      :model-value="value.time"
      @update:model-value="onTime"
      type="time"
      variant="outlined"
      density="compact"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  modelValue: { type: Object, default: () => ({ date: '', time: '' }) },
  label: { type: String, default: '' },
  rules: { type: Array, default: () => [] }, // правила на ВЕСЬ объект {date,time}
})

const emit = defineEmits(['update:modelValue'])
const menu = ref(false)

const value = computed(() => ({
  date: props.modelValue?.date || '',
  time: props.modelValue?.time || '',
}))

const dateRules = computed(() =>
  (props.rules || []).map((rule) => {
    if (typeof rule !== 'function') return () => true
    return () => rule(value.value)
  })
)

function formatLocalDate(d) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

function onPickDate(v) {
  let s = ''
  if (typeof v === 'string') s = v
  else if (v instanceof Date) s = formatLocalDate(v)
  else if (v) s = String(v).slice(0, 10)

  emit('update:modelValue', { ...value.value, date: s })
  menu.value = false
}

function onTime(t) {
  emit('update:modelValue', { ...value.value, time: t })
}
</script>
