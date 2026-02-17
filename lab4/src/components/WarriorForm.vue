<template>
  <form @submit.prevent="createWarrior">
    <h1>Создание война</h1>
    <input
      v-model="warrior.name"
      class="input"
      type="text"
      placeholder="Имя"
    />
    <input
      v-model="warrior.race"
      class="input"
      type="text"
      placeholder="Расса"
    />
    <button class="btn" type="submit">Создать</button>
  </form>
</template>

<script>
import { api, apiErrorMessage, isNetworkError } from '@/api'

export default {
  name: 'WarriorForm',
  props: {
    demoMode: { type: Boolean, default: false }
  },
  data() {
    return {
      warrior: {
        name: '',
        race: ''
      }
    }
  },
  methods: {
    async createWarrior() {
      const name = this.warrior.name?.trim()
      const race = this.warrior.race ?? ''
      try {
        await api.post('/warrior/create1', { race, name })
        this.warrior.name = ''
        this.warrior.race = ''
      } catch (e) {
        if (this.demoMode && isNetworkError(e)) {
          this.$emit('add-local', { name, race })
          this.warrior.name = ''
          this.warrior.race = ''
        } else {
          alert(apiErrorMessage(e))
        }
      }
    }
  }
}
</script>

<style scoped>
form {
  margin: 20px 0;
  padding: 16px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
</style>
