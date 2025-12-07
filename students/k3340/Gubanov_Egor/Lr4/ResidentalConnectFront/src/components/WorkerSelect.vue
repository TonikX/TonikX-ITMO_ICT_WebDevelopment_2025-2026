<template>
  <v-select
    v-model="selectedValue"
    :items="workers"
    item-title="displayName"
    item-value="id"
    :label="label"
    :required="required"
    :disabled="disabled"
    :error-messages="errorMessages"
    variant="outlined"
    prepend-inner-icon="mdi-account-wrench"
    @update:model-value="handleChange"
  >
    <template v-slot:item="{ props, item }">
      <v-list-item v-bind="props">
        <template v-slot:title>
          {{ item.raw.displayName }}
        </template>
        <template v-slot:subtitle v-if="item.raw.email">
          {{ item.raw.email }}
        </template>
      </v-list-item>
    </template>
  </v-select>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'WorkerSelect',
  props: {
    modelValue: {
      type: [Number, String],
      default: null,
    },
    label: {
      type: String,
      default: 'Мастер',
    },
    required: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    errorMessages: {
      type: Array,
      default: () => [],
    },
  },
  emits: ['update:modelValue'],
  data() {
    return {
      workers: [],
      loading: false,
    }
  },
  computed: {
    selectedValue: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      },
    },
  },
  async mounted() {
    await this.loadWorkers()
  },
  methods: {
    async loadWorkers() {
      this.loading = true
      try {
        const response = await api.get('/api/auth/users/', {
          params: { role: 'master' },
        })
        const users = response.data.results || response.data || []
        this.workers = users.map(user => ({
          ...user,
          displayName: user.first_name && user.last_name
            ? `${user.first_name} ${user.last_name} (${user.username})`
            : user.username,
        }))
      } catch (error) {
        console.error('Error loading workers:', error)
        this.workers = []
      } finally {
        this.loading = false
      }
    },
    handleChange(value) {
      this.$emit('update:modelValue', value)
    },
  },
}
</script>

