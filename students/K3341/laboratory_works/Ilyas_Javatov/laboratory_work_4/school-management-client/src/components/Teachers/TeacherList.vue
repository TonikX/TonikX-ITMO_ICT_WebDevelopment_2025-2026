<template>
  <v-card>
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-account-multiple</v-icon>
        Список учителей
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
            label="Поиск учителей"
            prepend-icon="mdi-magnify"
            variant="outlined"
            clearable
            @input="onSearch"
          />
        </v-col>
      </v-row>

      <v-data-table
        :headers="headers"
        :items="teachers"
        :loading="loading"
        :items-per-page="10"
        :search="search"
        class="elevation-1"
      >
        <template v-slot:item.actions="{ item }">
          <v-btn icon size="small" @click="$emit('edit', item)">
            <v-icon color="primary">mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon size="small" @click="$emit('view', item)">
            <v-icon color="info">mdi-eye</v-icon>
          </v-btn>
          <v-btn icon size="small" @click="$emit('delete', item)">
            <v-icon color="error">mdi-delete</v-icon>
          </v-btn>
        </template>

        <template v-slot:item.subjects="{ item }">
          <v-chip
            v-for="subject in (item.subjects_names || []).slice(0, 3)"
            :key="subject"
            size="small"
            class="mr-1 mb-1"
          >
            {{ subject }}
          </v-chip>
          <span v-if="(item.subjects_names || []).length > 3" class="text-caption text-grey">
            +{{ item.subjects_names.length - 3 }}
          </span>
        </template>

        <template v-slot:no-data>
          <div class="text-center py-6">
            <v-icon size="64" color="grey" class="mb-4">mdi-account-off</v-icon>
            <p class="text-h6 text-grey">Учителя не найдены</p>
            <p class="text-body-1 text-grey">Добавьте первого учителя</p>
          </div>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'TeacherList',
  props: {
    teachers: {
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
        { title: 'Фамилия', key: 'last_name' },
        { title: 'Имя', key: 'first_name' },
        { title: 'Предметы', key: 'subjects' },
        { title: 'Кабинет', key: 'classroom_number' },
        { title: 'Действия', key: 'actions', sortable: false, width: 150 }
      ]
    }
  },
  methods: {
    onSearch() {
      this.$emit('search', this.search)
    },
  }
}
</script>