<template>
  <v-text-field
    v-model="internalValue"
    :label="label"
    :placeholder="placeholder"
    :prepend-icon="prependIcon"
    :append-icon="appendIcon"
    :variant="variant"
    :density="density"
    :clearable="clearable"
    :loading="loading"
    :disabled="disabled"
    @input="onInput"
    @keyup.enter="onSearch"
    @click:clear="onClear"
  />
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    label: {
      type: String,
      default: 'Поиск'
    },
    placeholder: {
      type: String,
      default: 'Введите для поиска...'
    },
    prependIcon: {
      type: String,
      default: 'mdi-magnify'
    },
    appendIcon: {
      type: String,
      default: ''
    },
    variant: {
      type: String,
      default: 'outlined'
    },
    density: {
      type: String,
      default: 'comfortable'
    },
    clearable: {
      type: Boolean,
      default: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    debounce: {
      type: Number,
      default: 300
    }
  },
  data() {
    return {
      internalValue: this.modelValue,
      timeoutId: null
    }
  },
  watch: {
    modelValue(newVal) {
      this.internalValue = newVal
    }
  },
  methods: {
    onInput() {
      if (this.timeoutId) {
        clearTimeout(this.timeoutId)
      }

      this.timeoutId = setTimeout(() => {
        this.$emit('update:modelValue', this.internalValue)
        this.$emit('input', this.internalValue)
      }, this.debounce)
    },

    onSearch() {
      if (this.timeoutId) {
        clearTimeout(this.timeoutId)
      }
      this.$emit('update:modelValue', this.internalValue)
      this.$emit('search', this.internalValue)
    },

    onClear() {
      this.internalValue = ''
      this.$emit('update:modelValue', '')
      this.$emit('clear')
    }
  }
}
</script>