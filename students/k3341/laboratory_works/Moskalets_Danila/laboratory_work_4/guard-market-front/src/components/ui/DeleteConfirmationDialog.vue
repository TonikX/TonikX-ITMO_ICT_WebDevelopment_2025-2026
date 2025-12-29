<template>
  <v-dialog :model-value="dialog" max-width="400" @update:model-value="$emit('update:dialog', $event)">
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon icon="mdi-alert-circle-outline" color="error" class="mr-2"></v-icon>
        {{ title }}
      </v-card-title>
      <v-card-text>
        <p class="text-body-1 mb-4" v-html="message"></p>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn
            @click="$emit('close')"
            variant="text"
            :disabled="loading"
        >
          Отмена
        </v-btn>
        <v-btn
            @click="$emit('confirm')"
            color="error"
            :loading="loading"
            prepend-icon="mdi-delete"
        >
          Удалить
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
defineProps({
  dialog: {
    type: Boolean,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Подтвердите удаление'
  },
  message: {
    type: String,
    default: 'Вы уверены, что хотите удалить этот элемент? <br><strong>Это действие нельзя отменить.</strong>'
  }
})

defineEmits(['close', 'confirm', 'update:dialog'])
</script>