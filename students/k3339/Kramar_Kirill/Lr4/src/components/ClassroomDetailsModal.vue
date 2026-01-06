<template>
  <div class="modal">
    <div class="modal-content">
      <h3>Classroom Details</h3>

      <div class="details">
        <p><strong>Room Number:</strong> {{ room.number }}</p>
        <p><strong>Room Type:</strong> {{ room.type }}</p>
      </div>

      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    room: Object,
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
