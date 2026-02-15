<template>
  <div class="app-container">
    <header class="app-header">
      <select v-model="selectedClass" class="class-select" @change="fetchGrades">
        <option v-for="klass in classes" :key="klass.id" :value="klass.id">
          {{ klass.parallel }}-{{ klass.class_number }}
        </option>
      </select>
      <button
          @click="openCreateModal"
          class="add-grade-btn"
          :disabled="!students.length">
        Add Grade
      </button>
    </header>

    <main class="main-content">
      <div v-for="student in students" :key="student.id" class="student-grades">
        <h3>{{ student.first_name }} {{ student.last_name }}</h3>
        <table class="grades-table">
          <thead>
          <tr>
            <th>Subject</th>
            <th>Grade</th>
            <th>Average Grade</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="subject in subjects" :key="subject.id">
            <td>{{ subject.name }}</td>
            <td>
              <div v-if="getGrades(student.id, subject.id).length > 0">
                <span
                    v-for="grade in getGrades(student.id, subject.id)"
                    :key="grade.id"
                    class="grade-cell"
                    @click="openDetailsModal(grade)"
                >
                  {{ grade.grade || '-' }}
                </span>
              </div>
              <div v-else>-</div>
            </td>
            <td>
              {{ getAverageGrade(student.id, subject.id) }}
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <p v-if="students.length === 0">No students found for the selected class.</p>
    </main>

    <CreateGradeModal
        v-if="isCreateModalVisible"
        @close="closeModal"
        @save="fetchGrades"
    />
    <EditGradeModal
        v-if="isEditModalVisible"
        :grade="selectedGrade"
        @close="closeModal"
        @save="fetchGrades"
    />
    <GradeDetailsModal
        v-if="isDetailsModalVisible"
        :grade="selectedGrade"
        @close="closeModal"
        @edit="openEditModal"
        @delete="deleteGrade"
    />
  </div>
</template>

<script>
import API from "@/axios";
import CreateGradeModal from "../components/CreateGradeModal.vue";
import EditGradeModal from "../components/EditGradeModal.vue";
import GradeDetailsModal from "../components/GradeDetailsModal.vue";

export default {
  components: {
    CreateGradeModal,
    EditGradeModal,
    GradeDetailsModal,
  },
  data() {
    return {
      classes: [],
      students: [],
      subjects: [],
      grades: [],
      selectedClass: null,
      isCreateModalVisible: false,
      isEditModalVisible: false,
      isDetailsModalVisible: false,
      selectedGrade: null,
    };
  },
  methods: {
    async fetchClasses() {
      try {
        const response = await API.get("/classes/");
        this.classes = response.data;
        if (this.classes.length > 0) {
          this.selectedClass = this.classes[0].id;
          this.fetchGrades();
        }
      } catch (error) {
        console.error("Error fetching classes:", error);
      }
    },
    async fetchGrades() {
      try {
        this.students = [];
        this.subjects = [];
        this.grades = [];

        const [studentsResponse, gradesResponse, subjectsResponse] = await Promise.all([
          API.get(`/class/${this.selectedClass}/students/`),
          API.get("/grades/"),
          API.get("/subjects/"),
        ]);
        console.log('Students:', studentsResponse.data.Students);

        this.students = studentsResponse.data.Students;
        this.subjects = subjectsResponse.data;

        this.grades = gradesResponse.data
            .map(grade => {
              const student = this.students.find(student => student.id === grade.student);
              const subject = this.subjects.find(subject => subject.id === grade.subject);

              if (!student || !subject) {
                console.warn(`Grade with ID ${grade.id} skipped due to missing student or subject`);
                return null;
              }

              return {
                ...grade,
                student,
                subject,
              };
            })
            .filter(grade => grade !== null);

        this.$nextTick(() => {
          if (this.students.length === 0) {
            console.warn("No students found after class change");
          }
        });
      } catch (error) {
        console.error("Error fetching grades:", error);
      }
    },
    getGrades(studentId, subjectId) {
      return this.grades.filter(
          grade => grade.student && grade.student.id === studentId &&
              grade.subject && grade.subject.id === subjectId
      );
    },
    getAverageGrade(studentId, subjectId) {
      const gradesForSubject = this.getGrades(studentId, subjectId);
      if (gradesForSubject.length === 0) return '-';
      const sum = gradesForSubject.reduce((total, grade) => total + grade.grade, 0);
      return (sum / gradesForSubject.length).toFixed(2);
    },
    openCreateModal() {
      this.isCreateModalVisible = true;
    },
    openEditModal(grade) {
      this.selectedGrade = { ...grade };
      this.isDetailsModalVisible = false;
      this.isEditModalVisible = true;
    },
    openDetailsModal(grade) {
      if (grade) {
        this.selectedGrade = { ...grade };
        this.isDetailsModalVisible = true;
      }
    },
    closeModal() {
      this.isCreateModalVisible = false;
      this.isEditModalVisible = false;
      this.isDetailsModalVisible = false;
    },
    async deleteGrade(gradeId) {
      try {
        await API.delete(`/grades/${gradeId}/`);
        this.fetchGrades();
      } catch (error) {
        console.error("Error deleting grade:", error);
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

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.class-select {
  padding: 5px;
  font-size: 16px;
}

.add-grade-btn {
  padding: 5px 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.grades-table {
  width: 100%;
  border-collapse: collapse;
}

.grades-table th,
.grades-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.grade-cell {
  cursor: pointer;
  margin-right: 5px;
}

.grade-cell:hover {
  background-color: #f0f0f0;
}
</style>
