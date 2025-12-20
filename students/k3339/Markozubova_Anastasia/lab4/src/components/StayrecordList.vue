<script setup>
/* ===== PROPS ===== */
defineProps({
  bookings: {
    type: Array,
    required: true,
  },
});

/* ===== EMITS ===== */
defineEmits(["edit-booking", "delete-booking"]);
</script>

<template>
  <div>
    <v-card
      v-for="booking in bookings"
      :key="booking.id"
      class="mb-4"
    >
      <v-card-title>
        Бронирование №{{ booking.id }}
      </v-card-title>

      <v-card-text>
      <div><strong>Имя клиента:</strong> {{ booking.client_name }}</div>
      <div><strong>Фамилия клиента:</strong> {{ booking.client_lastname }}</div>
        <div><strong>Комната:</strong> {{ booking.room_number }}</div>
        <div>
          <strong>Даты:</strong>
          {{ booking.check_in_date }} — {{ booking.check_out_date }}
        </div>
        <div><strong>ID клиента:</strong> {{ booking.client }}</div>
        <div><strong>ID комнаты:</strong> {{ booking.room }}</div>
      </v-card-text>

      <v-card-actions>
        <v-btn
          color="primary"
          @click="$emit('edit-booking', booking)"
        >
          Редактировать
        </v-btn>

        <v-btn
          color="error"
          @click="$emit('delete-booking', booking.id)"
        >
          Удалить
        </v-btn>
      </v-card-actions>
    </v-card>

    <div v-if="!bookings.length">
      <p>Нет бронирований.</p>
    </div>
  </div>
</template>
