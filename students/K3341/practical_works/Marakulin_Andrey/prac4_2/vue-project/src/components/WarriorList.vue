<template>
  <div>
    <h2>Список воинов</h2>
    <div class="warrior" v-for="warrior in warriors" :key="warrior.name">
      <div><strong>Имя:</strong> {{ warrior.name }}</div>
      <div><strong>Расса:</strong> {{ warrior.race }}</div>
      <hr>
    </div>
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
  margin-bottom: 10px;
}
</style>