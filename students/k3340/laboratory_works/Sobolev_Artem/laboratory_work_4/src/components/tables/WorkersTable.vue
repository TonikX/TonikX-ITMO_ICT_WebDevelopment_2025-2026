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
          <img
              v-if="getHeaderKey(headerItem) === 'photo'"
              :src="row[getHeaderKey(headerItem)]"
              alt="Фото"
              style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%;"
          />
          <span v-else-if="getHeaderKey(headerItem) === 'name'">
            {{ row.lastName }} {{ row.firstName }} {{ row.patronymic }}
          </span>
          <span v-else-if="getHeaderKey(headerItem) === 'position'">
            {{ row.position }}
          </span>

          <span v-else-if="getHeaderKey(headerItem) === 'id'">
             <router-link :to="{ name: 'Сотрудник', params: { id: row.id } }">
               <Icon name="arrow-right" style="color: var(--color);"/>
             </router-link>
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
import {computed} from "vue";
import Icon from "@/components/ui/Icon.vue";

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
})

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