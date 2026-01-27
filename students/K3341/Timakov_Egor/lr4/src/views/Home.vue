<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h4">Добро пожаловать в систему управления типографией</v-card-title>
          <v-card-text>
            <p class="text-h6">Система предназначена для информационного обслуживания сотрудников типографии.</p>
            <v-divider class="my-4"></v-divider>
            <v-list>
              <v-list-item prepend-icon="mdi-account-group">
                <v-list-item-title>Управление сотрудниками</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-account-edit">
                <v-list-item-title>Управление авторами</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-book">
                <v-list-item-title>Управление книгами</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-cash">
                <v-list-item-title>Финансовый учёт</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-chart-box">
                <v-list-item-title>Отчёты и аналитика</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Home'
}
</script>
