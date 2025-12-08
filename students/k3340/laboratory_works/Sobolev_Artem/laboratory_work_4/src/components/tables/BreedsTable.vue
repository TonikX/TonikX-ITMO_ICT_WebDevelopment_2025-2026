<template>
  <div class="table">
    <table>
      <thead>
      <tr>
        <th v-for="(headerItem, index) in headersItem" :key="index">
          {{ getHeaderLabel(headerItem) }}
        </th>
      </tr>
      </thead>

      <tbody>
      <tr v-for="(row, rowIndex) in bodyRows" :key="rowIndex">
        <td
            v-for="(headerItem, colIndex) in headersItem"
            :key="colIndex"
        >
          {{ row[getHeaderKey(headerItem)] }}
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({
  heightSize: {
    type: Number,
    default: 5,
  },
  headersItem: {
    type: Array,
    required: true,
  },
  bodyItems: {
    type: Array,
    required: () => [],
  }
})

const bodyRows = computed(() => {
  return props.bodyItems.slice(0, props.heightSize)
});

const getHeaderKey = (headerItem) => {
  return typeof headerItem === 'object' ? headerItem.key : headerItem
}
const getHeaderLabel = (headerItem) => {
  return typeof headerItem === 'object' ? headerItem.label : headerItem
}
</script>

<style lang="scss" scoped>
table {
  width: 100%;
  border-collapse: collapse;
  background: var(--section-bg);
}

table {
  width: 100%;
  border-collapse: collapse;
}

table, th, td {
  border: 1px solid var(--sidebar-text);
  color: var(--color);
}

th, td {
  text-align: center;
  vertical-align: middle;
  padding: 8px;
}
</style>