<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Edit Grade</h2>
      <form @submit.prevent="updateGrade">
        <div class="form-group">
          <label for="subject">Subject:</label>
          <input type="text" id="subject" v-model="grade.subject.name" disabled />
        </div>

        <div class="form-group">
          <label for="grade">Grade:</label>
          <input
              type="number"
              v-model="updatedGrade"
              id="grade"
              min="1"
              max="5"
              required
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
  props: {
    grade: Object,
  },
  data() {
    return {
      updatedGrade: this.grade.grade,
    };
  },
  methods: {
    async updateGrade() {
      try {
        const gradeUpdate = {
          id: this.grade.id,
          grade: this.updatedGrade,
          student: this.grade.student.id,
          subject: this.grade.subject.id,
        };

        await API.put(`/grades/${this.grade.id}/`, gradeUpdate);

        this.$emit("save");
        this.$emit("close");
      } catch (error) {
        console.error("Error updating grade:", error);
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
  z-index: 1050;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
  z-index: 1060;
}

h2 {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-size: 16px;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
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

.cancel {
  background-color: #dc3545;
  color: white;
}

button:hover {
  opacity: 0.8;
}
</style>
