<template>
  <div>
    <div class="warrior" v-for="(warrior, index) in warriors" :key="index">
      <div><strong>Имя:</strong> {{ warrior.name }}</div>
      <div><strong>Расса:</strong> {{ warrior.race }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WarriorList',
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
  padding: 12px;
  margin-bottom: 12px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
</style>
