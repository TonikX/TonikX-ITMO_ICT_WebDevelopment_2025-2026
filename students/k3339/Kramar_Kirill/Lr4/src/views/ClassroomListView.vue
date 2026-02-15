<template>
  <div class="classrooms-container">
    <header>
      <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Search by room number or type"
      />
    </header>

    <button @click="openCreateModal" class="add-classroom-btn">Add Classroom</button>

    <main>
      <div v-if="filteredClassrooms.length > 0" class="classroom-list">
        <div
            v-for="room in filteredClassrooms"
            :key="room.id"
            class="classroom-card"
        >
          <div class="classroom-card-header">
            <h3>{{ room.number }} ({{ room.type }})</h3>
          </div>
          <div class="classroom-card-footer">
            <button @click="openEditModal(room)">Edit</button>
            <button @click="deleteClassroom(room.id)">Delete</button>
            <button @click="openDetailModal(room)">Details</button>
          </div>
        </div>
      </div>

      <div v-else>
        <p>No classrooms found.</p>
      </div>
    </main>

    <CreateClassroomModal
        v-if="isCreateModalVisible"
        @close="closeModal"
        @save="fetchClassrooms"
    />
    <EditClassroomModal
        v-if="isEditModalVisible"
        :room="selectedRoom"
        @close="closeModal"
        @save="fetchClassrooms"
    />
    <ClassroomDetailsModal
        v-if="isDetailModalVisible"
        :room="selectedRoom"
        @close="closeModal"
    />
  </div>
</template>

<script>
import API from "@/axios";
import CreateClassroomModal from "../components/CreateClassroomModal.vue";
import EditClassroomModal from "../components/EditClassroomModal.vue";
import ClassroomDetailsModal from "../components/ClassroomDetailsModal.vue";

export default {
  components: {
    CreateClassroomModal,
    EditClassroomModal,
    ClassroomDetailsModal,
  },
  data() {
    return {
      classrooms: [],
      searchQuery: "",
      isCreateModalVisible: false,
      isEditModalVisible: false,
      isDetailModalVisible: false,
      selectedRoom: null,
    };
  },
  computed: {
    filteredClassrooms() {
      return this.classrooms.filter((room) =>
          `${room.number} ${room.type}`.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    async fetchClassrooms() {
      try {
        const response = await API.get("/classrooms/");
        this.classrooms = response.data;
      } catch (error) {
        console.error("Error fetching classrooms:", error);
      }
    },
    openCreateModal() {
      this.selectedRoom = null;
      this.isCreateModalVisible = true;
    },
    openEditModal(room) {
      this.selectedRoom = {...room};
      this.isEditModalVisible = true;
    },
    openDetailModal(room) {
      this.selectedRoom = {...room};
      this.isDetailModalVisible = true;
    },
    closeModal() {
      this.isCreateModalVisible = false;
      this.isEditModalVisible = false;
      this.isDetailModalVisible = false;
    },
    async deleteClassroom(roomId) {
      try {
        await API.delete(`/classrooms/${roomId}/`);
        this.classrooms = this.classrooms.filter((room) => room.id !== roomId);
      } catch (error) {
        console.error("Error deleting classroom:", error);
      }
    },
  },
  mounted() {
    this.fetchClassrooms();
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
