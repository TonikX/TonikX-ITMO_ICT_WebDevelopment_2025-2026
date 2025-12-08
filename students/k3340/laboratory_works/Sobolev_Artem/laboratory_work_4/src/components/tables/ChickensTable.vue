<template>
  <div class="table">
    <table>
      <thead>
      <tr>
        <th v-for="(headerItem, index) in headersItem" :key="index">
          <div class="header-cell">
            <span>{{ getHeaderLabel(headerItem) }}</span>
            <Button
                v-if="isSortable(getHeaderKey(headerItem))"
                mode="sort"
                :is-active="sortKey === getHeaderKey(headerItem)"
                @click="$emit('sort', getHeaderKey(headerItem))"
            >
              <ArrowDownNarrowWide :size="16" />
            </Button>
          </div>
        </th>
      </tr>
      </thead>

      <tbody>
      <tr v-for="(row, rowIndex) in bodyRows" :key="rowIndex">
        <td v-for="(headerItem, colIndex) in headersItem" :key="colIndex">
          <img
              v-if="getHeaderKey(headerItem) === 'photo'"
              :src="row[getHeaderKey(headerItem)]"
              alt="Фото"
              style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%;"
          />

          <span v-else-if="getHeaderKey(headerItem) === 'id'">
            {{ row[getHeaderKey(headerItem)] }}
          </span>

          <span v-else-if="getHeaderKey(headerItem) === 'link'">
            <router-link :to="{ name: 'Курица', params: { id: row.id } }">
              <Icon name="arrow-right" style="color: var(--color);" />
            </router-link>
          </span>

          <span v-else-if="getHeaderKey(headerItem) === 'breedId'">
            {{ row.breedName || row.breed?.name || 'Не указана' }}
          </span>

          <span v-else>
            {{ formattedCell(row, getHeaderKey(headerItem)) }}
          </span>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import {computed} from "vue";
import Icon from "@/components/ui/Icon.vue";
import Button from "@/components/ui/Button.vue";
import {formatDate} from "@/utils/formatDate.js";
import { ArrowDownNarrowWide } from 'lucide-vue-next';

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
  },
  sortKey: {
    type: String,
    default: null
  }
})

defineEmits(['sort']);

const bodyRows = computed(() => {
  return props.bodyItems.slice(0, props.heightSize)
});

const formattedCell = (row, key) => {
  if (key === 'birthDate') return row.birthDate ? formatDate(row.birthDate) : '';
  return row[key];
};

const getHeaderKey = (headerItem) => {
  return typeof headerItem === 'object' ? headerItem.key : headerItem
}
const getHeaderLabel = (headerItem) => {
  return typeof headerItem === 'object' ? headerItem.label : headerItem
}

const isSortable = (key) => {
  const sortableKeys = ['id', 'name', 'breedName', 'weight', 'eggs', 'age', 'birthDate'];
  return sortableKeys.includes(key);
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

.header-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>