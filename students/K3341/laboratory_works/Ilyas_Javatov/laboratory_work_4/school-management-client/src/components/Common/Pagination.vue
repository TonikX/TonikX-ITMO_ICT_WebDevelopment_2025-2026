<template>
  <div class="d-flex align-center justify-space-between mt-4">
    <div class="text-caption text-grey">
      Показано {{ startItem }}-{{ endItem }} из {{ totalItems }}
    </div>

    <v-pagination
      v-model="currentPage"
      :length="totalPages"
      :total-visible="visiblePages"
      @update:model-value="onPageChange"
    />

    <div class="d-flex align-center gap-2">
      <span class="text-caption text-grey">На странице:</span>
      <v-select
        v-model="itemsPerPage"
        :items="pageSizeOptions"
        density="compact"
        variant="outlined"
        hide-details
        style="width: 80px;"
        @update:model-value="onPageSizeChange"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    modelValue: {
      type: Number,
      default: 1
    },
    totalItems: {
      type: Number,
      default: 0
    },
    itemsPerPage: {
      type: Number,
      default: 10
    },
    visiblePages: {
      type: Number,
      default: 5
    },
    pageSizeOptions: {
      type: Array,
      default: () => [5, 10, 25, 50, 100]
    }
  },
  data() {
    return {
      currentPage: this.modelValue
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage)
    },
    startItem() {
      return (this.currentPage - 1) * this.itemsPerPage + 1
    },
    endItem() {
      const end = this.currentPage * this.itemsPerPage
      return end > this.totalItems ? this.totalItems : end
    }
  },
  watch: {
    modelValue(newVal) {
      this.currentPage = newVal
    }
  },
  methods: {
    onPageChange(page) {
      this.$emit('update:modelValue', page)
      this.$emit('page-change', page)
    },

    onPageSizeChange(size) {
      this.$emit('page-size-change', size)
      // Сбрасываем на первую страницу при изменении размера страницы
      this.currentPage = 1
      this.$emit('update:modelValue', 1)
    }
  }
}
</script>