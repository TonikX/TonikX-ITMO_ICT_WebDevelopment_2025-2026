<template>
  <div class="app">
    <h1>Портал информации о войнах в онлайн РПГ</h1>

    <div v-if="demoMode" class="demo-banner">
      Режим демо: API недоступен, данные локальные. Когда сервер заработает — нажмите «Получить список войнов».
    </div>

    <button class="btn" v-on:click="fetchWarriors">Получить список войнов</button>
    <WarriorForm :demo-mode="demoMode" @add-local="addLocalWarrior" />
    <WarriorList v-bind:warriors="warriors" />
  </div>
</template>

<script>
import WarriorForm from '@/components/WarriorForm.vue'
import WarriorList from '@/components/WarriorList.vue'
import { api, isNetworkError, apiErrorMessage } from '@/api'

const MOCK_WARRIORS = [
  { name: 'Арагорн', race: 'Человек' },
  { name: 'Леголас', race: 'Эльф' }
]

export default {
  name: 'Warriors',
  components: {
    WarriorForm,
    WarriorList
  },
  data() {
    return {
      warriors: [],
      demoMode: false
    }
  },
  methods: {
    async fetchWarriors() {
      try {
        const response = await api.get('/warriors/list/')
        this.warriors = response.data?.results ?? response.data ?? []
        this.demoMode = false
      } catch (e) {
        if (isNetworkError(e)) {
          this.demoMode = true
          this.warriors = [...MOCK_WARRIORS]
        } else {
          this.warriors = []
          alert(apiErrorMessage(e))
        }
      }
    },
    addLocalWarrior({ name, race }) {
      if (name?.trim()) this.warriors.push({ name: name.trim(), race: race || '' })
    }
  },
  mounted() {
    this.fetchWarriors()
  }
}
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.demo-banner {
  padding: 10px 14px;
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 6px;
  color: #856404;
  font-size: 14px;
}
</style>
