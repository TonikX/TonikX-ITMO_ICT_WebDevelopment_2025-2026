<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title class="text-h4 mb-4">Дополнительные запросы</v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-card
              class="pa-4"
              color="surface-variant"
              variant="tonal"
              to="/requests/n_free_rooms"
            >
              <v-card-title>
                <v-icon class="mr-2">mdi-bed-empty</v-icon>
                Свободные номера
              </v-card-title>
              <v-card-text>
                Количество свободных номеров на текущий момент
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card
              class="pa-4"
              color="surface-variant"
              variant="tonal"
              to="/requests/guests_by_city"
            >
              <v-card-title>
                <v-icon class="mr-2">mdi-city</v-icon>
                Гости по городу
              </v-card-title>
              <v-card-text>
                Количество гостей из определённого города
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card
              class="pa-4"
              color="surface-variant"
              variant="tonal"
              to="/requests/guests_by_room_period"
            >
              <v-card-title>
                <v-icon class="mr-2">mdi-account-group</v-icon>
                Гости по номеру и периоду
              </v-card-title>
              <v-card-text>
                Список гостей, проживавших в номере за определённый период
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card
              class="pa-4"
              color="surface-variant"
              variant="tonal"
              to="/requests/guests_by_guest_period"
            >
              <v-card-title>
                <v-icon class="mr-2">mdi-account-multiple</v-icon>
                Гости в тот же период
              </v-card-title>
              <v-card-text>
                Гости, проживавшие в отеле в тот же период, что и выбранный гость
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card
              class="pa-4"
              color="surface-variant"
              variant="tonal"
              to="/requests/staff_by_guest_day"
            >
              <v-card-title>
                <v-icon class="mr-2">mdi-broom</v-icon>
                Сотрудник по гостю и дню
              </v-card-title>
              <v-card-text>
                Сотрудник, который убирал номер клиента в заданный день
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card
              class="pa-4"
              color="surface-variant"
              variant="tonal"
              to="/requests/quarterly_report"
            >
              <v-card-title>
                <v-icon class="mr-2">mdi-chart-bar</v-icon>
                Квартальный отчёт
              </v-card-title>
              <v-card-text>
                Отчёт по доходам и загрузке отеля за квартал
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
</script>
