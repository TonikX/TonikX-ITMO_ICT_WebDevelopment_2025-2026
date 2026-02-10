<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import BookingModal from "@/components/StayrecordModal.vue";
import BookingList from "@/components/StayrecordList.vue";
import { tokenStore } from "@/stores/token.js";

const token = tokenStore();

const bookings = ref([]);
const clients = ref([]);
const rooms = ref([]);
const isModalVisible = ref(false);
const selectedBooking = ref(null);
const isLoading = ref(true);

async function fetchBookings() {
  try {
    const { data } = await axios.get("/api/stay-records/", {
      headers: { Authorization: `Token ${token.token}` },
    });
    bookings.value = data;
  } catch (e) {
    console.error("Ошибка загрузки бронирований", e);
  } finally {
    isLoading.value = false;
  }
}

async function fetchClients() {
  const { data } = await axios.get("/api/clients/", {
    headers: { Authorization: `Token ${token.token}` },
  });
  clients.value = data;
}

async function fetchRooms() {
  const { data } = await axios.get("/api/rooms/", {
    headers: { Authorization: `Token ${token.token}` },
  });
  rooms.value = data;
}

async function saveBooking(booking) {
  try {
    if (booking.id) {
      await axios.patch(
        `/api/stay-records/${booking.id}/`,
        booking,
        { headers: { Authorization: `Token ${token.token}` } }
      );
    } else {
      await axios.post(
        "/api/stay-records/",
        booking,
        { headers: { Authorization: `Token ${token.token}` } }
      );
    }

    await fetchBookings();
    isModalVisible.value = false;
  } catch (e) {
    console.error("Ошибка сохранения бронирования", e);
  }
}

async function deleteBooking(id) {
  await axios.delete(`/api/stay-records/${id}/`, {
    headers: { Authorization: `Token ${token.token}` },
  });
  await fetchBookings();
}

function handleEditBooking(booking) {
  selectedBooking.value = { ...booking };
  isModalVisible.value = true;
}

function handleAddBooking() {
  selectedBooking.value = null;
  isModalVisible.value = true;
}

onMounted(async () => {
  await Promise.all([
    fetchBookings(),
    fetchClients(),
    fetchRooms()
  ]);
});
</script>

<template>
  <v-container>
    <v-skeleton-loader
      v-if="isLoading"
      type="card"
      class="mt-4"
      max-width="500"
    />

    <template v-else>
      <h2>Список бронирований</h2>

      <v-btn color="primary" class="mb-4" @click="handleAddBooking">
        Добавить бронирование
      </v-btn>

      <BookingList
        :bookings="bookings"
        @edit-booking="handleEditBooking"
        @delete-booking="deleteBooking"
      />

      <BookingModal
        v-model="isModalVisible"
        :booking="selectedBooking"
        :rooms="rooms"
        :clients="clients"
        @save-booking="saveBooking"
      />
    </template>
  </v-container>
</template>
