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
            :style="getSeasonCellStyle(getHeaderKey(headerItem), row[getHeaderKey(headerItem)])"
        >
          {{ formatSeason(getHeaderKey(headerItem), row[getHeaderKey(headerItem)]) }}
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

const getSeasonCellStyle = (key, value) => {
  if (key !== 'season') return {};

  const seasonColors = {
    'WINTER': '#079BFE',
    'SPRING': '#68CF93',
    'SUMMER': '#FD684B',
    'AUTUMN': '#FFA95F'
  }

  return {
    backgroundColor: seasonColors[value] || 'transparent',
    color: 'white',
    fontWeight: '600',
  };
};

const formatSeason = (key, value) => {
  if (key !== "season") return value;

  const seasonMap = {
    WINTER: "Зима",
    SPRING: "Весна",
    SUMMER: "Лето",
    AUTUMN: "Осень",
  };

  return seasonMap[value?.toUpperCase()] || value;
};
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