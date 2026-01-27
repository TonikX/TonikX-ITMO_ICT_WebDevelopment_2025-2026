<template>
  <div class="warrior-list">
    <div class="warrior" v-for="warrior in warriors" :key="warrior.id"> <!-- v-for - директива для отображения списка элементов на основе массива. -->
      <div><strong>Имя:</strong> {{ warrior.name }}</div>
      <div><strong>Расса:</strong> {{ warrior.race }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "WarriorList",
  props: { // «Props» -- это специальное ключевое слово, обозначающее свойства . Его можно зарегистрировать в дочернем компоненте для передачи данных от родительского компонента к одному из его дочерних компонентов.
    warriors: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
.warrior {
  border: 1px solid #ccc;
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
}
</style>