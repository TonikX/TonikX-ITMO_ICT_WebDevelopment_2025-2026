<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Edit Lesson</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="subject">Subject</label>
          <select v-model="form.subject" id="subject" required>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="class">Class</label>
          <select v-model="form.klass" id="class" required>
            <option v-for="klass in classes" :key="klass.id" :value="klass.id">
              {{ klass.parallel }}-{{ klass.class_number }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="weekday">Weekday</label>
          <select v-model="form.weekday" id="weekday" required>
            <option v-for="day in weekdays" :key="day" :value="day">{{ day }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="lesson_number">Lesson Number</label>
          <input type="number" v-model="form.lesson_number" id="lesson_number" required />
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
  props: {
    lesson: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: { ...this.lesson },
      subjects: [],
      classes: [],
      weekdays: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    };
  },
  methods: {
    async fetchData() {
      try {
        const [subjectsResponse, classesResponse] = await Promise.all([
          API.get("/subjects/"),
          API.get("/classes/"),
        ]);
        this.subjects = subjectsResponse.data;
        this.classes = classesResponse.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async submitForm() {
      try {
        await API.put(`/lessons/${this.lesson.id}/`, this.form);
        this.$emit("save");
        this.$emit("close");
      } catch (error) {
        console.error("Error updating lesson:", error);
      }
    },
  },
  watch: {
    lesson(newLesson) {
      this.form = { ...newLesson };
    }
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
