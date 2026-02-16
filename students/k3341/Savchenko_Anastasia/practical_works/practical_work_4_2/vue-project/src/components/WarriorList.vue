<template>
  <div>
    <h2>Список войнов</h2>
    <ul>
      <li v-for="warrior in warriors" :key="warrior.id">
        {{ warrior.name }} ({{ warrior.race }})
      </li>
    </ul>
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
</style>