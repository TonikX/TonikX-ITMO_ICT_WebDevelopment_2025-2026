<template>
  <v-card>
    <v-card-title v-if="title" class="d-flex align-center">
      <span>{{ title }}</span>
      <v-spacer></v-spacer>
      <slot name="actions"></slot>
    </v-card-title>
    <v-card-text>
      <v-data-table
        :headers="headers"
        :items="items"
        :loading="loading"
        :items-per-page="itemsPerPage"
        :items-per-page-options="itemsPerPageOptions"
        :server-items-length="totalItems"
        @update:options="handleOptionsUpdate"
        class="elevation-0"
      >
        <template v-slot:item="{ item }">
          <tr>
            <td v-for="header in headers" :key="header.key">
              <slot :name="`item.${header.key}`" :item="item">
                {{ getNestedValue(item, header.key) }}
              </slot>
            </td>
          </tr>
        </template>
        <template v-slot:no-data>
          <div class="text-center py-8">
            <v-icon size="64" color="grey-lighten-1">mdi-database-off</v-icon>
            <div class="text-h6 mt-4 text-grey">Нет данных</div>
          </div>
        </template>
        <template v-slot:loading>
          <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    headers: {
      type: Array,
      required: true,
    },
    items: {
      type: Array,
      default: () => [],
    },
    loading: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: '',
    },
    itemsPerPage: {
      type: Number,
      default: 20,
    },
    itemsPerPageOptions: {
      type: Array,
      default: () => [10, 20, 50, 100],
    },
    totalItems: {
      type: Number,
      default: 0,
    },
  },
  emits: ['update:options'],
  methods: {
    getNestedValue(obj, path) {
      return path.split('.').reduce((current, prop) => current?.[prop], obj) ?? ''
    },
    handleOptionsUpdate(options) {
      this.$emit('update:options', options)
    },
  },
}
</script>

