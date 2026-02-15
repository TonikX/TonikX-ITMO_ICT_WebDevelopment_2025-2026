<template>
  <div class="app-container">
    <header class="app-header">
      <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Search students by name or class"
      />
    </header>

    <button @click="openCreateModal" class="add-student-btn">Add Student</button>

    <main class="main-content">
      <div v-if="filteredStudents.length > 0" class="student-list">
        <div
            v-for="student in filteredStudents"
            :key="student.id"
            class="student-card"
        >
          <div class="student-card-header">
            <h3>{{ student.full_name }}</h3>
          </div>
          <div class="student-card-body">
            <p><strong>Class:</strong> {{ student.class_name }}</p>
            <p><strong>Gender:</strong> {{ student.gender }}</p>
          </div>
          <div class="student-card-footer">
            <button @click="openEditModal(student)">Edit</button>
            <button @click="deleteStudent(student.id)">Delete</button>
          </div>
        </div>
      </div>

      <div v-else>
        <p>No students found.</p>
      </div>
    </main>

    <CreateStudentModal
        v-if="isCreateModalVisible"
        @close="closeModal"
        @save="fetchStudents"
    />

    <EditStudentModal
        v-if="isEditModalVisible"
        :student="selectedStudent"
        @close="closeModal"
        @save="fetchStudents"
    />
  </div>
</template>

<script>
import API from "@/axios";
import CreateStudentModal from "../components/CreateStudentModal.vue";
import EditStudentModal from "../components/EditStudentModal.vue";

export default {
  components: {
    CreateStudentModal,
    EditStudentModal,
  },
  data() {
    return {
      students: [],
      searchQuery: "",
      isCreateModalVisible: false,
      isEditModalVisible: false,
      selectedStudent: null,
    };
  },
  computed: {
    filteredStudents() {
      return this.students.filter((student) =>
          student.full_name
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase()) ||
          student.class_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await API.get("/students/");
        const studentsData = response.data;
        const classesResponse = await API.get("/classes/");
        const classes = classesResponse.data.reduce((map, klass) => {
          map[klass.id] = klass;
          return map;
        }, {});
        this.students = studentsData.map((student) => ({
          ...student,
          full_name: `${student.first_name} ${student.last_name} ${student.middle_name || ""}`.trim(),
          class_name: student.klass && classes[student.klass]
              ? `${classes[student.klass].parallel}-${classes[student.klass].class_number}`
              : "No Class",
        }));
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    },
    async deleteStudent(studentId) {
      try {
        await API.delete(`/students/${studentId}/`);
        this.students = this.students.filter((student) => student.id !== studentId);
      } catch (error) {
        console.error("Error deleting student:", error);
      }
    },
    openCreateModal() {
      this.selectedStudent = null;
      this.isCreateModalVisible = true;
    },
    openEditModal(student) {
      this.selectedStudent = {...student};
      this.isEditModalVisible = true;
    },
    closeModal() {
      this.isCreateModalVisible = false;
      this.isEditModalVisible = false;
    },
  },
  mounted() {
    this.fetchStudents();
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
