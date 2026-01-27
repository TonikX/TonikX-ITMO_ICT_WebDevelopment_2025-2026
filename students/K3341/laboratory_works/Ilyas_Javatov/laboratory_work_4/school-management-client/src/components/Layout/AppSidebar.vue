<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-list>
      <v-list-item
        prepend-icon="mdi-view-dashboard"
        title="Панель управления"
        value="dashboard"
        to="/dashboard"
      />
    </v-list>

    <v-divider />

    <v-list>
      <v-list-group value="management">
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-cog"
            title="Управление"
          />
        </template>

        <v-list-item
          prepend-icon="mdi-account-multiple"
          title="Учителя"
          value="teachers"
          to="/teachers"
        />

        <v-list-item
          prepend-icon="mdi-school"
          title="Ученики"
          value="students"
          to="/students"
        />

        <v-list-item
          prepend-icon="mdi-google-classroom"
          title="Классы"
          value="classes"
          to="/classes"
        />

        <v-list-item
          prepend-icon="mdi-door"
          title="Кабинеты"
          value="classrooms"
          to="/classrooms"
        />
      </v-list-group>

      <v-list-item
        prepend-icon="mdi-calendar"
        title="Расписание"
        value="schedule"
        to="/schedule"
      />

      <v-list-group value="reports">
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-chart-bar"
            title="Отчеты"
          />
        </template>

        <v-list-item
          prepend-icon="mdi-chart-line"
          title="Успеваемость"
          value="performance"
          to="/reports?type=performance"
        />

        <v-list-item
          prepend-icon="mdi-gender-male-female"
          title="Статистика по полу"
          value="gender"
          to="/reports?type=gender"
        />

        <v-list-item
          prepend-icon="mdi-door"
          title="Кабинеты"
          value="classrooms-report"
          to="/reports?type=classrooms"
        />
      </v-list-group>

      <v-list-item
        prepend-icon="mdi-file-document"
        title="Документация"
        href="http://localhost:9999/"
        target="_blank"
      />
    </v-list>

    <template v-slot:append>
      <div class="pa-4">
        <v-divider class="mb-4" />
        <div class="text-center">
          <v-chip color="grey-lighten-3" variant="flat" size="small">
            Версия 1.0.0
          </v-chip>
        </div>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'AppSidebar',
  props: {
    modelValue: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    drawer: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  }
}
</script>