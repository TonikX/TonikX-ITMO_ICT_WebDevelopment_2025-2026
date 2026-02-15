<template>
  <div class="modal">
    <div class="modal-content">
      <h3>Edit Student</h3>

      <form @submit.prevent="updateStudent">
        <div class="form-group">
          <label for="first_name">First Name</label>
          <input v-model="student.first_name" type="text" id="first_name" required />
        </div>

        <div class="form-group">
          <label for="last_name">Last Name</label>
          <input v-model="student.last_name" type="text" id="last_name" required />
        </div>

        <div class="form-group">
          <label for="middle_name">Middle Name</label>
          <input v-model="student.middle_name" type="text" id="middle_name" />
        </div>

        <div class="form-group">
          <label for="gender">Gender</label>
          <select v-model="student.gender" required>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </div>

        <div class="form-group">
          <label for="klass">Class</label>
          <select v-model="student.klass" required>
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
  props: {
    student: Object,
  },
  data() {
    return {
      klasses: [],
    };
  },
  methods: {
    async fetchKlasses() {
      try {
        const response = await API.get('/classes/');
        this.klasses = response.data;
      } catch (error) {
        console.error('Error fetching classes:', error);
      }
    },
    async updateStudent() {
      const studentData = { ...this.student };
      try {
        await API.put(`/students/${this.student.id}/`, studentData);
        this.$emit('save');
        this.$emit('close');
      } catch (error) {
        console.error('Error updating student:', error);
      }
    },
  },
  created() {
    this.fetchKlasses();
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
