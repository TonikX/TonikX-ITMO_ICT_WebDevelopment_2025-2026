<template>
  <v-card>
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-google-classroom</v-icon>
        Список классов
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
            label="Поиск классов"
            prepend-icon="mdi-magnify"
            variant="outlined"
            clearable
            @input="onSearch"
          />
        </v-col>
      </v-row>

      <v-data-table
        :headers="headers"
        :items="classes"
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
          <v-btn icon size="small" @click="$emit('report', item)">
            <v-icon color="success">mdi-chart-bar</v-icon>
          </v-btn>
          <v-btn icon size="small" @click="$emit('delete', item)">
            <v-icon color="error">mdi-delete</v-icon>
          </v-btn>
        </template>

        <template v-slot:item.students_count="{ item }">
          <v-chip :color="getStudentCountColor(item.students_count)" variant="flat">
            {{ item.students_count }} учеников
          </v-chip>
        </template>

        <template v-slot:item.class_teacher_name="{ item }">
          <v-chip v-if="item.class_teacher_name" color="info" variant="flat">
            {{ item.class_teacher_name }}
          </v-chip>
          <span v-else class="text-grey">Не назначен</span>
        </template>

        <template v-slot:no-data>
          <div class="text-center py-6">
            <v-icon size="64" color="grey" class="mb-4">mdi-google-classroom</v-icon>
            <p class="text-h6 text-grey">Классы не найдены</p>
            <p class="text-body-1 text-grey">Добавьте первый класс</p>
          </div>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ClassList',
  props: {
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
      headers: [
        { title: 'ID', key: 'id', width: 80 },
        { title: 'Название класса', key: 'class_name' },
        { title: 'Классный руководитель', key: 'class_teacher_name' },
        { title: 'Количество учеников', key: 'students_count' },
        { title: 'Действия', key: 'actions', sortable: false, width: 200 }
      ]
    }
  },
  methods: {
    getStudentCountColor(count) {
      if (count === 0) return 'grey'
      if (count < 15) return 'warning'
      if (count < 30) return 'info'
      return 'success'
    },
    onSearch() {
      this.$emit('search', this.search)
    }
  }
}
</script>