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
        <td v-for="(headerItem, colIndex) in headersItem" :key="colIndex">
          <span v-if="getHeaderKey(headerItem) === 'breedAvgEggs'">
            {{ formatEggs(row[getHeaderKey(headerItem)]) }}
          </span>

          <span v-else-if="getHeaderKey(headerItem) === 'farmAvgEggs'">
            {{ formatEggs(row[getHeaderKey(headerItem)]) }}
          </span>

          <span v-else-if="getHeaderKey(headerItem) === 'diffEggs'">
            <span :class="getDiffClass(row[getHeaderKey(headerItem)])">
              {{ formatDiff(row[getHeaderKey(headerItem)]) }}
            </span>
          </span>

          <span v-else-if="getHeaderKey(headerItem) === 'performance'">
            <span :class="getPerformanceClass(row.diffEggs)">
              {{ getPerformanceText(row.diffEggs) }}
            </span>
          </span>

          <span v-else>
            {{ row[getHeaderKey(headerItem)] }}
          </span>
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

const bodyRows = computed(() => props.bodyItems.slice(0, props.heightSize));

const getHeaderKey = (headerItem) => typeof headerItem === 'object' ? headerItem.key : headerItem;
const getHeaderLabel = (headerItem) => typeof headerItem === 'object' ? headerItem.label : headerItem;

const formatEggs = (eggs) => {
  if (eggs === null || eggs === undefined) return '0';
  return `${eggs.toFixed(1)} яиц`;
};

const formatDiff = (diff) => {
  if (diff === null || diff === undefined) return '0';
  const sign = diff >= 0 ? '+' : '';
  return `${sign}${diff.toFixed(1)} яиц`;
};

const getDiffClass = (diff) => {
  if (diff > 0) return 'positive-diff';
  if (diff < 0) return 'negative-diff';
  return 'neutral-diff';
};

const getPerformanceClass = (diff) => {
  if (diff > 50) return 'performance-excellent';
  if (diff > 20) return 'performance-good';
  if (diff > 0) return 'performance-average';
  if (diff < -20) return 'performance-poor';
  return 'performance-below-avg';
};

const getPerformanceText = (diff) => {
  if (diff > 50) return 'Отлично';
  if (diff > 20) return 'Хорошо';
  if (diff > 0) return 'Средне';
  if (diff < -20) return 'Плохо';
  return 'Ниже среднего';
};
</script>

<style lang="scss" scoped>
.table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: var(--section-bg);
  min-width: 800px;
}

table, th, td {
  border: 1px solid var(--sidebar-text);
  color: var(--color);
}

th, td {
  text-align: center;
  vertical-align: middle;
  padding: 12px 8px;
}

th {
  font-weight: 600;
  background: var(--background);
}

tr:hover {
  background: var(--background);
}

.positive-diff {
  color: #4caf50;
  font-weight: 600;
}

.negative-diff {
  color: #f44336;
  font-weight: 600;
}

.neutral-diff {
  color: var(--color);
}

.performance-excellent {
  color: #4caf50;
  font-weight: 600;
  background: rgba(76, 175, 80, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}

.performance-good {
  color: #8bc34a;
  font-weight: 600;
  background: rgba(139, 195, 74, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}

.performance-average {
  color: #ffc107;
  font-weight: 600;
  background: rgba(255, 193, 7, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}

.performance-below-avg {
  color: #ff9800;
  font-weight: 600;
  background: rgba(255, 152, 0, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}

.performance-poor {
  color: #f44336;
  font-weight: 600;
  background: rgba(244, 67, 54, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}
</style>