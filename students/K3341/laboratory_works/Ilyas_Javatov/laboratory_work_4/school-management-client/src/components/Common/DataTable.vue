<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :loading="loading"
    :items-per-page="itemsPerPage"
    :search="search"
    class="elevation-1"
    @update:options="onOptionsUpdate"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title v-if="title">{{ title }}</v-toolbar-title>
        <v-spacer />

        <v-text-field
          v-if="showSearch"
          v-model="search"
          :label="searchLabel"
          prepend-icon="mdi-magnify"
          variant="outlined"
          density="compact"
          clearable
          class="mr-4"
          style="max-width: 300px;"
        />

        <slot name="toolbar-actions" />
      </v-toolbar>
    </template>

    <template v-slot:item.actions="{ item }">
      <div class="d-flex gap-1">
        <slot name="item-actions" :item="item" />
      </div>
    </template>

    <template v-slot:no-data>
      <div class="text-center py-6">
        <v-icon size="64" color="grey" class="mb-4">{{ emptyIcon }}</v-icon>
        <p class="text-h6 text-grey">{{ emptyText || 'Данные не найдены' }}</p>
        <p v-if="emptySubtext" class="text-body-1 text-grey">{{ emptySubtext }}</p>
        <slot name="no-data-actions" />
      </div>
    </template>

    <template v-slot:loading>
      <div class="text-center py-6">
        <v-progress-circular indeterminate />
        <p class="mt-4">Загрузка данных...</p>
      </div>
    </template>

    <template v-for="(_, slotName) in $slots" v-slot:[slotName]="slotData">
      <slot :name="slotName" v-bind="slotData" />
    </template>
  </v-data-table>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    headers: {
      type: Array,
      default: () => []
    },
    items: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    itemsPerPage: {
      type: Number,
      default: 10
    },
    title: {
      type: String,
      default: ''
    },
    showSearch: {
      type: Boolean,
      default: true
    },
    searchLabel: {
      type: String,
      default: 'Поиск'
    },
    emptyText: {
      type: String,
      default: ''
    },
    emptySubtext: {
      type: String,
      default: ''
    },
    emptyIcon: {
      type: String,
      default: 'mdi-database-off'
    }
  },
  data() {
    return {
      search: ''
    }
  },
  methods: {
    onOptionsUpdate(options) {
      this.$emit('options-update', options)
    }
  }
}
</script>