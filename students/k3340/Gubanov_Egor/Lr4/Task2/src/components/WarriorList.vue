<template>
  <div class="warrior" v-for="warrior in warriors">
    <div><strong>Имя:</strong> {{ warrior.name }}</div>
    <div><strong>Расса:</strong> {{ warrior.race }}</div>
  </div>
</template>

<script>
export default {
  props: {
    warriors: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
.warrior {
  background-color: #f5f5f5;
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
  border-left: 4px solid #42b983;
}
</style>

