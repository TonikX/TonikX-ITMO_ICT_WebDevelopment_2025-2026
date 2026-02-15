<template>
  <div class="app-container">
    <header class="app-header">
      <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Search teachers by name"
      />
    </header>

    <button @click="openCreateModal" class="add-teacher-btn">Add Teacher</button>

    <main class="main-content">
      <div v-if="filteredTeachers.length > 0" class="teacher-list">
        <div
            v-for="teacher in filteredTeachers"
            :key="teacher.id"
            class="teacher-card"
        >
          <div class="teacher-card-header">
            <h3>{{ teacher.full_name }}</h3>
          </div>
          <div class="teacher-card-body">
            <p><strong>Subjects:</strong> {{ teacher.subjects.join(", ") }}</p>
            <p v-if="teacher.class_name"><strong>Class:</strong> {{ teacher.class_name }}</p>
            <p v-if="teacher.classroom"><strong>Classroom:</strong> {{ teacher.classroom.number }}</p>
          </div>
          <div class="teacher-card-footer">
            <button @click="openEditModal(teacher)">Edit</button>
            <button @click="deleteTeacher(teacher.id)">Delete</button>
          </div>
        </div>
      </div>

      <div v-else>
        <p>No teachers found.</p>
      </div>
    </main>

    <CreateTeacherModal
        v-if="isCreateModalVisible"
        @close="closeModal"
        @save="fetchTeachers"
        @teacherUpdated="fetchTeachers"
    />

    <EditTeacherModal
        v-if="isEditModalVisible"
        :teacher="selectedTeacher"
        @close="closeModal"
        @save="fetchTeachers"
        @teacherUpdated="fetchTeachers"
    />
  </div>
</template>

<script>
import API from "@/axios";
import CreateTeacherModal from "../components/CreateTeacherModal.vue";
import EditTeacherModal from "../components/EditTeacherModal.vue";

export default {
  components: {
    CreateTeacherModal,
    EditTeacherModal,
  },
  data() {
    return {
      teachers: [],
      searchQuery: "",
      isCreateModalVisible: false,
      isEditModalVisible: false,
      selectedTeacher: null,
    };
  },
  computed: {
    filteredTeachers() {
      return this.teachers.filter((teacher) =>
          teacher.full_name
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    async fetchTeachers() {
      try {
        const response = await API.get("/teachers/");
        if (response.data) {
          this.teachers = response.data.map((teacher) => ({
            ...teacher,
            full_name: `${teacher.first_name} ${teacher.last_name} ${teacher.middle_name || ""}`.trim(),
            subjects: teacher.subject.map((subject) => subject.name),
            class_name: teacher.klass
                ? `${teacher.klass.parallel}-${teacher.klass.class_number}`
                : null,
            classroom: teacher.classroom ? teacher.classroom : null,
          }));
        } else {
          console.error("Unexpected API response structure:", response.data);
          this.teachers = [];
        }
      } catch (error) {
        console.error("Error fetching teachers:", error);
      }
    },
    async deleteTeacher(teacherId) {
      try {
        await API.delete(`/teachers/${teacherId}/`);
        this.teachers = this.teachers.filter((teacher) => teacher.id !== teacherId);
      } catch (error) {
        console.error("Error deleting teacher:", error);
      }
    },
    openCreateModal() {
      this.selectedTeacher = null;
      this.isCreateModalVisible = true;
    },
    openEditModal(teacher) {
      this.selectedTeacher = { ...teacher };
      this.isEditModalVisible = true;
    },
    closeModal() {
      this.isCreateModalVisible = false;
      this.isEditModalVisible = false;
    },
  },
  mounted() {
    this.fetchTeachers();
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
