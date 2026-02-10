<script setup>

import router from "@/router/index.js";

defineProps({
  rooms: Array,
  isRoomFree: Function
});

function getRoomType(type) {
    const types = {
        single: "Одиночная",
        double: "Двухместная",
        triple: "Трёхместная"
    }
    return types[type] || "Unknown";
}


</script>

<template>
  <div>
    <template v-for="floor in [1, 2, 3, 4, 5]" :key="floor">
      <h3>Этаж {{ floor }}</h3>
      <div class="floor">
        <template v-for="room in rooms.filter((roomObj) => roomObj.floor === floor)" :key="room.id">
          <v-card
              :color="isRoomFree(room) ? 'green lighten-3' : 'red lighten-3'"
              class="room-card"
              @click="router.push(`/rooms/${room.id}`)">
            <v-card-title class="room-title">
              Комната №{{ room.number }}
            </v-card-title>
            <v-card-subtitle class="room-details">
              Тип: {{ getRoomType(room.room_type) }}<br/>
              Стоимость: {{ room.price_per_day }} ₽/сутки
            </v-card-subtitle>
          </v-card>
        </template>
      </div>
    </template>
  </div>
</template>

<style scoped>
.floor {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.room-card {
  width: 250px;
  padding: 16px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.room-card:hover {
  transform: scale(1.05);
}

.room-title {
  font-weight: bold;
  font-size: 18px;
}

.room-details {
  font-size: 14px;
  line-height: 1.6;
  white-space: normal;
}
</style>