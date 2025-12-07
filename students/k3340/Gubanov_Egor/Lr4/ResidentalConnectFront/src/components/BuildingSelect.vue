<template>
  <v-select
    v-model="selectedValue"
    :items="buildings"
    item-title="address"
    item-value="id"
    :label="label"
    :required="required"
    :disabled="disabled"
    :error-messages="errorMessages"
    variant="outlined"
    prepend-inner-icon="mdi-office-building"
    @update:model-value="handleChange"
  >
    <template v-slot:item="{ props, item }">
      <v-list-item v-bind="props">
        <template v-slot:title>
          {{ item.raw.address }}
        </template>
        <template v-slot:subtitle v-if="item.raw.total_floors">
          {{ item.raw.total_floors }} этажей
        </template>
      </v-list-item>
    </template>
  </v-select>
</template>

<script>
import { buildingsService } from '@/services/buildingsService'

export default {
  name: 'BuildingSelect',
  props: {
    modelValue: {
      type: [Number, String],
      default: null,
    },
    label: {
      type: String,
      default: 'Дом',
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
      buildings: [],
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
    await this.loadBuildings()
  },
  methods: {
    async loadBuildings() {
      this.loading = true
      try {
        const data = await buildingsService.getBuildings()
        this.buildings = data.results || data || []
      } catch (error) {
        console.error('Error loading buildings:', error)
        this.buildings = []
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

