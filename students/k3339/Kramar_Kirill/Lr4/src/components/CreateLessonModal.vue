<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Create Lesson</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="subject">Subject</label>
          <select v-model="form.subject.id" id="subject" required>
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

        <div class="form-group">
          <label for="teacher">Teacher</label>
          <select v-model="form.teacher.id" id="teacher" required>
            <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
              {{ teacher.first_name }} {{ teacher.last_name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="classroom">Classroom</label>
          <select v-model="form.classroom.id" id="classroom" required>
            <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id">
              {{ classroom.number }} ({{ classroom.type }})
            </option>
          </select>
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
      form: {
        subject: {id: null, name: "", subject_type: ""},
        klass: null,
        weekday: "",
        lesson_number: null,
        teacher: {id: null, first_name: "", last_name: "", klass: null, classroom: null, subject: []},
        classroom: {id: null, number: "", type: ""}
      },
      subjects: [],
      classes: [],
      teachers: [],
      classrooms: [],
      weekdays: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    };
  },
  methods: {
    async fetchData() {
      try {
        const [subjectsResponse, classesResponse, teachersResponse, classroomsResponse] = await Promise.all([
          API.get("/subjects/"),
          API.get("/classes/"),
          API.get("/teachers/"),
          API.get("/classrooms/"),
        ]);
        this.subjects = subjectsResponse.data;
        this.classes = classesResponse.data;
        this.teachers = teachersResponse.data;
        this.classrooms = classroomsResponse.data;
        console.log('Classrooms data:', this.classrooms);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },

    async submitForm() {
      try {
        const lessonData = {
          subject: this.form.subject.id,
          klass: this.form.klass,
          weekday: this.form.weekday,
          lesson_number: this.form.lesson_number,
          teacher: this.form.teacher.id,
          classroom: this.form.classroom.id,
        };

        await API.post("/lessons/", lessonData);
        this.$emit("save");
        this.$emit("close");
      } catch (error) {
        console.error("Error creating lesson:", error);
      }
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
