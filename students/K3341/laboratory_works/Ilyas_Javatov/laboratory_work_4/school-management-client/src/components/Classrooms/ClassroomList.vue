<template>
  <v-card>
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-door</v-icon>
        Список кабинетов
      </v-toolbar-title>
      <v-spacer />
      <v-btn color="success" @click="$emit('add')">
        <v-icon left>mdi-plus</v-icon>
        Добавить
      </v-btn>
    </v-toolbar>

    <v-card-text>
      <v-row class="mb-4">
        <v-col cols="12" md="6">
          <v-text-field
            v-model="search"
            label="Поиск кабинетов"
            prepend-icon="mdi-magnify"
            variant="outlined"
            clearable
            @input="onSearch"
          />
        </v-col>
      </v-row>

      <v-data-table
        :headers="headers"
        :items="classrooms"
        :loading="loading"
        :items-per-page="10"
        :search="search"
        class="elevation-1"
      >
        <template v-slot:item.subject_type="{ item }">
          <v-chip :color="item.subject_type === 'profile' ? 'purple' : 'blue'" variant="flat">
            {{ item.subject_type === 'profile' ? 'Профильные' : 'Базовые' }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon size="small" @click="$emit('edit', item)">
            <v-icon color="primary">mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon size="small" @click="$emit('delete', item)">
            <v-icon color="error">mdi-delete</v-icon>
          </v-btn>
        </template>

        <template v-slot:no-data>
          <div class="text-center py-6">
            <v-icon size="64" color="grey" class="mb-4">mdi-door</v-icon>
            <p class="text-h6 text-grey">Кабинеты не найдены</p>
            <p class="text-body-1 text-grey">Добавьте первый кабинет</p>
          </div>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ClassroomList',
  props: {
    classrooms: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      search: '',
      headers: [
        { title: 'ID', key: 'id', width: 80 },
        { title: 'Номер кабинета', key: 'room_number' },
        { title: 'Тип', key: 'subject_type' },
        { title: 'Действия', key: 'actions', sortable: false, width: 140 }
      ]
    }
  },
  methods: {
    onSearch() {
      this.$emit('search', this.search)
    }
  }
}
</script>
