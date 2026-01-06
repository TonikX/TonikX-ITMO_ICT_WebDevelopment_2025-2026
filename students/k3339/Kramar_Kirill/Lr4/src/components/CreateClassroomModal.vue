<template>
  <div class="modal">
    <div class="modal-content">
      <h3>Add Classroom</h3>

      <form @submit.prevent="createClassroom">
        <div class="form-group">
          <label for="number">Room Number</label>
          <input v-model="room.number" type="text" id="number" required />
        </div>

        <div class="form-group">
          <label for="type">Room Type</label>
          <input v-model="room.type" type="text" id="type" required />
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
      room: {
        number: '',
        type: '',
      },
    };
  },
  methods: {
    async createClassroom() {
      try {
        await API.post("/classrooms/", this.room);
        this.$emit("save");
        this.$emit("close");
      } catch (error) {
        console.error("Error creating classroom:", error);
      }
    },
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
