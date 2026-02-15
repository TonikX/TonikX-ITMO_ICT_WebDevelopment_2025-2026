<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Create Grade</h2>
      <form @submit.prevent="createGrade">
        <div class="form-group">
          <label for="student-select">Student:</label>
          <select v-model="selectedStudent" id="student-select" required>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.first_name }} {{ student.last_name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="subject-select">Subject:</label>
          <select v-model="selectedSubject" id="subject-select" required>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="teacher-select">Teacher:</label>
          <select v-model="selectedTeacher" id="teacher-select" required>
            <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
              {{ teacher.first_name }} {{ teacher.last_name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="grade-input">Grade:</label>
          <input
              type="number"
              v-model="grade"
              id="grade-input"
              min="1"
              max="5"
              required
              placeholder="Enter grade"
          />
        </div>

        <button type="submit" class="btn">Save</button>
        <button type="button" class="btn cancel" @click="$emit('close')">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
import API from "@/axios";

export default {
  data() {
    return {
      students: [],
      subjects: [],
      teachers: [],
      selectedStudent: null,
      selectedSubject: null,
      selectedTeacher: null,
      grade: null,
    };
  },
  async mounted() {
    try {
      const [studentsResponse, subjectsResponse, teachersResponse] = await Promise.all([
        API.get("/students/"),
        API.get("/subjects/"),
        API.get("/teachers/"),
      ]);

      this.students = studentsResponse.data;
      this.subjects = subjectsResponse.data;
      this.teachers = teachersResponse.data;
    } catch (error) {
      console.error("Error loading data:", error);
    }
  },
  methods: {
    async createGrade() {
      if (this.selectedStudent && this.selectedSubject && this.selectedTeacher && this.grade) {
        try {
          await API.post("/grades/", {
            student: this.selectedStudent,
            subject: this.selectedSubject,
            teacher: this.selectedTeacher,
            grade: this.grade,
          });
          this.$emit("save");
          this.$emit("close");
        } catch (error) {
          console.error("Error creating grade:", error);
        }
      } else {
        alert("Please fill all fields.");
      }
    },
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
