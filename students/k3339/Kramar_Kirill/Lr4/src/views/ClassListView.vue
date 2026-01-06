<template>
  <div class="classes-container">
    <header>
      <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Search by class or parallel"
      />
    </header>

    <button @click="openCreateModal" class="add-class-btn">Add Class</button>

    <main>
      <div v-if="filteredClasses.length > 0" class="class-list">
        <div
            v-for="klass in filteredClasses"
            :key="klass.id"
            class="class-card"
        >
          <div class="class-card-header">
            <!-- Отображаем параллель и номер класса -->
            <h3>{{ klass.parallel }}-{{ klass.class_number }}</h3>
          </div>
          <div class="class-card-footer">
            <button @click="openEditModal(klass)">Edit</button>
            <button @click="deleteClass(klass.id)">Delete</button>
            <button @click="openDetailModal(klass)">Details</button>
          </div>
        </div>
      </div>

      <div v-else>
        <p>No classes found.</p>
      </div>
    </main>

    <CreateClassModal
        v-if="isCreateModalVisible"
        @close="closeModal"
        @save="fetchClasses"
    />
    <EditClassModal
        v-if="isEditModalVisible"
        :klass="selectedClass"
        @close="closeModal"
        @save="fetchClasses"
    />
    <ClassDetailsModal
        v-if="isDetailModalVisible"
        :klass="selectedClass"
        @close="closeModal"
    />
  </div>
</template>

<script>
import API from "@/axios";
import CreateClassModal from "../components/CreateClassModal.vue";
import EditClassModal from "../components/EditClassModal.vue";
import ClassDetailsModal from "../components/ClassDetailsModal.vue";

export default {
  components: {
    CreateClassModal,
    EditClassModal,
    ClassDetailsModal,
  },
  data() {
    return {
      classes: [],
      searchQuery: "",
      isCreateModalVisible: false,
      isEditModalVisible: false,
      isDetailModalVisible: false,
      selectedClass: null,
      teachers: [],
    };
  },
  computed: {
    filteredClasses() {
      return this.classes.filter((klass) =>
          `${klass.parallel}-${klass.class_number}`
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    async fetchClasses() {
      try {
        const response = await API.get("/classes/");
        this.classes = response.data;
      } catch (error) {
        console.error("Error fetching classes:", error);
      }
    },
    openCreateModal() {
      this.selectedClass = null;
      this.isCreateModalVisible = true;
    },
    openEditModal(klass) {
      this.selectedClass = {...klass};
      this.isEditModalVisible = true;
    },
    openDetailModal(klass) {
      this.selectedClass = {...klass};
      this.isDetailModalVisible = true;
    },
    closeModal() {
      this.isCreateModalVisible = false;
      this.isEditModalVisible = false;
      this.isDetailModalVisible = false;
    },
    async deleteClass(classId) {
      try {
        await API.delete(`/classes/${classId}/`);
        this.classes = this.classes.filter((klass) => klass.id !== classId);
      } catch (error) {
        console.error("Error deleting class:", error);
      }
    },
  },
  mounted() {
    this.fetchClasses();
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
