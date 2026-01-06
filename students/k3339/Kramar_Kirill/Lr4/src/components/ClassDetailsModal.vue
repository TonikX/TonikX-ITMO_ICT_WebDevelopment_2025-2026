<template>
  <div class="modal">
    <div class="modal-content">
      <h3>Class Details</h3>

      <div class="details">
        <p><strong>Class Name:</strong> {{ klass.parallel }}-{{ klass.class_number }}</p>
        <p><strong>Class Teacher:</strong> {{ klassTeacherName }}</p>
        <p><strong>Number of Students:</strong> {{ studentCount }}</p>
      </div>

      <div class="gender-summary">
        <h4>Gender Summary:</h4>
        <p><strong>Boys:</strong> {{ klassGenderCount.boys }}</p>
        <p><strong>Girls:</strong> {{ klassGenderCount.girls }}</p>
      </div>

      <div class="students">
        <h4>Students:</h4>
        <ul>
          <li v-for="student in students" :key="student.id">
            {{ student.first_name }} {{ student.last_name }}
          </li>
        </ul>
      </div>

      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script>
import API from "@/axios";

export default {
  props: {
    klass: Object,
  },
  data() {
    return {
      teacher: null,
      students: [],
      genderCounts: {},
    };
  },
  computed: {
    klassTeacherName() {
      if (this.teacher) {
        return `${this.teacher.first_name} ${this.teacher.last_name}`;
      } else if (this.teacher === null) {
        return "Loading teacher...";
      } else {
        return "Failed to load teacher";
      }
    },
    studentCount() {
      return this.students.length;
    },
    klassGenderCount() {
      if (this.genderCounts[this.klass.id]) {
        const { boys, girls } = this.genderCounts[this.klass.id];
        return { boys, girls };
      }
      return { boys: 0, girls: 0 };
    },
  },
  methods: {
    async fetchTeacher() {
      try {
        const teacherResponse = await API.get(`/teachers/${this.klass.class_teacher}/`);
        this.teacher = teacherResponse.data;
      } catch (error) {
        console.error("Error fetching teacher:", error);
        this.teacher = false;
      }
    },
    async fetchStudents() {
      try {
        const studentResponse = await API.get(`/class/${this.klass.id}/students/`);
        this.students = studentResponse.data.Students;
      } catch (error) {
        console.error("Error fetching students:", error);
        this.students = [];
      }
    },
    async fetchGenderCounts() {
      try {
        const response = await API.get('/classes/gender/count/');
        this.genderCounts = response.data.GenderCounts;
      } catch (error) {
        console.error('Error fetching gender counts:', error);
        this.genderCounts = {};
      }
    },
  },
  created() {
    this.fetchTeacher();
    this.fetchStudents();
    this.fetchGenderCounts();
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";

.students {
  margin-top: 1rem;
}

.students h4 {
  margin-bottom: 0.5rem;
}

.students ul {
  list-style-type: disc;
  margin-left: 1.5rem;
}

.gender-summary {
  margin-top: 1rem;
}
</style>
