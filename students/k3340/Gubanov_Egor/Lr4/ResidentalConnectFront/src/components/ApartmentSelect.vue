<template>
  <v-select
    v-model="selectedValue"
    :items="apartments"
    item-title="displayName"
    item-value="id"
    :label="label"
    :required="required"
    :disabled="disabled"
    :error-messages="errorMessages"
    variant="outlined"
    prepend-inner-icon="mdi-home"
    @update:model-value="handleChange"
  >
    <template v-slot:item="{ props, item }">
      <v-list-item v-bind="props">
        <template v-slot:title>
          {{ item.raw.displayName }}
        </template>
        <template v-slot:subtitle v-if="item.raw.building">
          {{ item.raw.building.address }}
        </template>
      </v-list-item>
    </template>
  </v-select>
</template>

<script>
import { apartmentsService } from '@/services/apartmentsService'

export default {
  name: 'ApartmentSelect',
  props: {
    modelValue: {
      type: [Number, String],
      default: null,
    },
    label: {
      type: String,
      default: 'Квартира',
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
    buildingId: {
      type: [Number, String],
      default: null,
    },
  },
  emits: ['update:modelValue'],
  data() {
    return {
      apartments: [],
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
  watch: {
    buildingId: {
      handler() {
        this.loadApartments()
      },
      immediate: true,
    },
  },
  async mounted() {
    await this.loadApartments()
  },
  methods: {
    async loadApartments() {
      this.loading = true
      try {
        const params = {}
        if (this.buildingId) {
          params.building = this.buildingId
        }
        const data = await apartmentsService.getApartments(params)
        const results = data.results || data
        this.apartments = results.map(apt => ({
          ...apt,
          displayName: `Кв. ${apt.number}, ${apt.building?.address || ''}`,
        }))
      } catch (error) {
        console.error('Error loading apartments:', error)
        this.apartments = []
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

