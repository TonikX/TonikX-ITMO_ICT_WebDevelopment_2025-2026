<template>
  <v-select
    v-model="selectedValue"
    :items="categories"
    item-title="name"
    item-value="id"
    :label="label"
    :required="required"
    :disabled="disabled"
    :error-messages="errorMessages"
    variant="outlined"
    prepend-inner-icon="mdi-tag"
    @update:model-value="handleChange"
  >
    <template v-slot:item="{ props, item }">
      <v-list-item v-bind="props">
        <template v-slot:title>
          {{ item.raw.name }}
        </template>
        <template v-slot:subtitle v-if="item.raw.description">
          {{ item.raw.description }}
        </template>
      </v-list-item>
    </template>
  </v-select>
</template>

<script>
import { categoriesService } from '@/services/categoriesService'

export default {
  name: 'CategorySelect',
  props: {
    modelValue: {
      type: [Number, String],
      default: null,
    },
    label: {
      type: String,
      default: 'Категория услуги',
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
      categories: [],
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
    await this.loadCategories()
  },
  methods: {
    async loadCategories() {
      this.loading = true
      try {
        const data = await categoriesService.getCategories()
        this.categories = Array.isArray(data) ? data : data.results || []
      } catch (error) {
        console.error('Error loading categories:', error)
        this.categories = []
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

