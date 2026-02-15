<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Grade Details</h2>
      <p><strong>Student:</strong> {{ grade.student.first_name }} {{ grade.student.last_name }}</p>
      <p><strong>Subject:</strong> {{ grade.subject.name }}</p>
      <p><strong>Grade:</strong> {{ grade.grade }}</p>

      <div class="modal-buttons">
        <button @click="$emit('edit', grade)" class="btn">Edit</button>
        <button @click="deleteGrade" class="btn delete">Delete</button>
        <button @click="$emit('close')" class="btn cancel">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import API from "@/axios";

export default {
  props: {
    grade: Object,
  },
  methods: {
    async deleteGrade() {
      if (confirm("Are you sure you want to delete this grade?")) {
        try {
          await API.delete(`/grades/${this.grade.id}/`);
          this.$emit("save");
          this.$emit("close");
        } catch (error) {
          console.error("Error deleting grade:", error);
        }
      }
    },
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1030;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
  z-index: 1040;
}

h2 {
  margin-bottom: 20px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
}

.btn {
  background-color: #28a745;
  color: white;
}

.delete {
  background-color: #dc3545;
  color: white;
}

.cancel {
  background-color: #6c757d;
  color: white;
}

button:hover {
  opacity: 0.8;
}
</style>
