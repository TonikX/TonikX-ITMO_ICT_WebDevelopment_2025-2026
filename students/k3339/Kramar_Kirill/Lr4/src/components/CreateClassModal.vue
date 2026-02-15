<template>
  <div class="modal">
    <div class="modal-content">
      <h3>Add Class</h3>

      <form @submit.prevent="createClass">
        <div class="form-group">
          <label for="parallel">Parallel</label>
          <input v-model="klass.parallel" type="number" id="parallel" required />
        </div>

        <div class="form-group">
          <label for="class_number">Class Number</label>
          <input v-model="klass.class_number" type="text" id="class_number" required />
        </div>

        <div class="form-group">
          <label for="class_teacher">Class Teacher</label>
          <select v-model="klass.class_teacher" required>
            <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
              {{ teacher.first_name }} {{ teacher.last_name }}
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
      klass: {
        parallel: '',
        class_number: '',
        class_teacher: null,
      },
      teachers: [],
    };
  },
  methods: {
    async fetchTeachers() {
      try {
        const response = await API.get("/teachers/");
        this.teachers = response.data.map(teacher => ({
          id: teacher.id,
          first_name: teacher.first_name,
          last_name: teacher.last_name,
        }));
      } catch (error) {
        console.error("Error fetching teachers:", error);
      }
    },
    async createClass() {
      try {
        await API.post("/classes/", this.klass);
        this.$emit("save");
        this.$emit("close");
      } catch (error) {
        console.error("Error creating class:", error);
      }
    },
  },
  created() {
    this.fetchTeachers();
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
