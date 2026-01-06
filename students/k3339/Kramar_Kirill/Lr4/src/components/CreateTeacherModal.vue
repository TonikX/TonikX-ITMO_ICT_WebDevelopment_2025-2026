<template>
  <div class="modal">
    <div class="modal-content">
      <h3>Add Teacher</h3>

      <form @submit.prevent="createTeacher">
        <div class="form-group">
          <label for="first_name">First Name</label>
          <input v-model="teacher.first_name" type="text" id="first_name" required />
        </div>

        <div class="form-group">
          <label for="last_name">Last Name</label>
          <input v-model="teacher.last_name" type="text" id="last_name" required />
        </div>

        <div class="form-group">
          <label for="middle_name">Middle Name</label>
          <input v-model="teacher.middle_name" type="text" id="middle_name" />
        </div>

        <div class="form-group">
          <label for="subjects">Subjects</label>
          <select v-model="selectedSubjects" multiple>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="classroom">Classroom</label>
          <select v-model="teacher.classroom">
            <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id">
              {{ classroom.number }} - {{ classroom.type }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="class_lead">Class Lead</label>
          <select v-model="teacher.class_lead">
            <option v-for="klass in klasses" :key="klass.id" :value="klass.id">
              {{ klass.parallel }}-{{ klass.class_number }}
            </option>
          </select>
        </div>

        <button type="submit">Save</button>
      </form>

      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script>
import API from "@/axios";

export default {
  data() {
    return {
      teacher: {
        first_name: '',
        last_name: '',
        middle_name: '',
        classroom: null,
        class_lead: null
      },
      subjects: [],
      classrooms: [],
      klasses: [],
      selectedSubjects: []
    };
  },
  methods: {
    async fetchSubjects() {
      try {
        const response = await API.get('/subjects/');
        this.subjects = response.data;
      } catch (error) {
        console.error('Error fetching subjects:', error);
      }
    },
    async fetchClassrooms() {
      try {
        const response = await API.get('/classrooms/');
        this.classrooms = response.data;
      } catch (error) {
        console.error('Error fetching classrooms:', error);
      }
    },
    async fetchKlasses() {
      try {
        const response = await API.get('/classes/');
        this.klasses = response.data;
      } catch (error) {
        console.error('Error fetching classes:', error);
      }
    },
    async createTeacher() {
      const teacherData = {
        ...this.teacher,
        klass: this.teacher.class_lead,
        subject: this.selectedSubjects.length > 0 ? this.selectedSubjects : []
      };

      try {
        await API.post('/teachers/', teacherData);
        this.$emit('teacherUpdated');
        this.$emit('close');
      } catch (error) {
        console.error('Error creating teacher:', error);
      }
    }
  },
  created() {
    this.fetchSubjects();
    this.fetchClassrooms();
    this.fetchKlasses();
  }
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
