<template>
  <v-card>
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-school</v-icon>
        Список учеников
      </v-toolbar-title>
      <v-spacer />
      <v-btn color="success" @click="$emit('add')">
        <v-icon left>mdi-plus</v-icon>
        Добавить
      </v-btn>
    </v-toolbar>

    <v-card-text>
      <v-row class="mb-4">
        <v-col cols="12" md="4">
          <v-text-field
            v-model="search"
            label="Поиск учеников"
            prepend-icon="mdi-magnify"
            variant="outlined"
            clearable
            @input="onSearch"
          />
        </v-col>
        <v-col cols="12" md="4">
          <v-select
            v-model="filters.gender"
            :items="genderOptions"
            label="Пол"
            variant="outlined"
            clearable
            @update:model-value="applyFilters"
          />
        </v-col>
        <v-col cols="12" md="4">
          <v-select
            v-model="filters.school_class"
            :items="classes"
            item-title="class_name"
            item-value="id"
            label="Класс"
            variant="outlined"
            clearable
            @update:model-value="applyFilters"
          />
        </v-col>
      </v-row>

      <v-data-table
        :headers="headers"
        :items="students"
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
          <v-btn icon size="small" @click="$emit('grades', item)">
            <v-icon color="success">mdi-chart-bar</v-icon>
          </v-btn>
          <v-btn icon size="small" @click="$emit('delete', item)">
            <v-icon color="error">mdi-delete</v-icon>
          </v-btn>
        </template>

        <template v-slot:item.gender="{ item }">
          <v-chip :color="item.gender === 'M' ? 'blue' : 'pink'" variant="flat">
            {{ item.gender === 'M' ? 'Мужской' : 'Женский' }}
          </v-chip>
        </template>

        <template v-slot:item.average_grade="{ item }">
          <v-chip
            :color="getGradeColor(item.average_grade)"
            variant="flat"
          >
            {{ item.average_grade ? item.average_grade.toFixed(1) : 'Нет оценок' }}
          </v-chip>
        </template>

        <template v-slot:no-data>
          <div class="text-center py-6">
            <v-icon size="64" color="grey" class="mb-4">mdi-school-off</v-icon>
            <p class="text-h6 text-grey">Ученики не найдены</p>
            <p class="text-body-1 text-grey">Добавьте первого ученика</p>
          </div>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'StudentList',
  props: {
    students: {
      type: Array,
      default: () => []
    },
    classes: {
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
      filters: {
        gender: null,
        school_class: null
      },
      genderOptions: [
        { title: 'Мужской', value: 'M' },
        { title: 'Женский', value: 'F' }
      ],
      headers: [
        { title: 'ID', key: 'id', width: 80 },
        { title: 'Фамилия', key: 'last_name' },
        { title: 'Имя', key: 'first_name' },
        { title: 'Пол', key: 'gender' },
        { title: 'Класс', key: 'class_name' },
        { title: 'Средний балл', key: 'average_grade' },
        { title: 'Действия', key: 'actions', sortable: false, width: 200 }
      ]
    }
  },
  methods: {
    getGradeColor(grade) {
      if (!grade) return 'grey'
      if (grade >= 4.5) return 'success'
      if (grade >= 3.5) return 'warning'
      return 'error'
    },
    onSearch() {
      this.$emit('search', this.search)
    },
    applyFilters() {
      this.$emit('filter', this.filters)
    }
  }
}
</script>