<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Lesson Details</h2>
      <p v-if="lesson.subject"><strong>Subject:</strong> {{ lesson.subject.name }}</p>
      <p v-if="lesson.class_name"><strong>Class:</strong> {{ lesson.class_name }}</p>
      <p v-if="lesson.teacher">
        <strong>Teacher:</strong> {{ lesson.teacher.first_name }} {{ lesson.teacher.last_name }}
      </p>
      <p v-if="lesson.weekday"><strong>Weekday:</strong> {{ lesson.weekday }}</p>
      <p v-if="lesson.lesson_number"><strong>Lesson Number:</strong> {{ lesson.lesson_number }}</p>

      <!-- New section for Classroom -->
      <p v-if="lesson.classroom"><strong>Classroom:</strong> {{ lesson.classroom.number }}</p>

      <div class="lesson-actions">
        <button @click="editLesson">Edit</button>
        <button @click="deleteLesson">Delete</button>
      </div>

      <button @click="$emit('close')" class="btn cancel">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    lesson: {
      type: Object,
      required: true,
    },
  },
  methods: {
    editLesson() {
      this.$emit('edit', this.lesson);
    },
    deleteLesson() {
      this.$emit('delete', this.lesson.id);
    }
  }
};
</script>

<style scoped>
@import "@/assets/styles.css";

.lesson-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.lesson-actions button {
  padding: 5px 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.lesson-actions button:hover {
  background-color: #0056b3;
}
</style>
