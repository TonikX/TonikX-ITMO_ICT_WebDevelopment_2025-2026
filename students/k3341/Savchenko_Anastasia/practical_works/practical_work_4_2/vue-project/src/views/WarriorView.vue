<template>
  <div>
    <h1>Управление войнами</h1>
    <button @click="fetchWarriors">Получить список войнов</button>
    <WarriorForm />
    <WarriorList :warriors="warriors" />
  </div>
</template>

<script>
import axios from 'axios'
import WarriorForm from '@/components/WarriorForm.vue'
import WarriorList from '@/components/WarriorList.vue'

export default {
  name: 'WarriorView',
  components: {
    WarriorForm,
    WarriorList
  },
  data() {
    return {
      warriors: []
    }
  },
  methods: {
    async fetchWarriors() {
      try {
        const response = await axios.get('http://62.109.28.95:8890/warriors/list/')
        this.warriors = response.data.results
      } catch (error) {
        console.error(error)
        alert('Ошибка при загрузке данных')
      }
    }
  }
}
</script>

<style scoped>
</style>