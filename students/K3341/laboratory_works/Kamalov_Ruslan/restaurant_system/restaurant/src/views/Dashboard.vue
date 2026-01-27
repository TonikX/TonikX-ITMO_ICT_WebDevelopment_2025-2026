<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Панель управления рестораном</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6" lg="3">
        <v-card class="text-center" color="primary" dark @click="$router.push('/employees')">
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-account-group</v-icon>
            <div class="text-h6">Сотрудники</div>
            <div class="text-body-2">Управление персоналом</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="3">
        <v-card class="text-center" color="success" dark @click="$router.push('/ingredients')">
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-food-apple</v-icon>
            <div class="text-h6">Ингредиенты</div>
            <div class="text-body-2">Склад и поставки</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="3">
        <v-card class="text-center" color="warning" dark @click="$router.push('/dishes')">
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-silverware-fork-knife</v-icon>
            <div class="text-h6">Блюда</div>
            <div class="text-body-2">Меню ресторана</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="3">
        <v-card class="text-center" color="info" dark @click="$router.push('/tables')">
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-table-furniture</v-icon>
            <div class="text-h6">Столы</div>
            <div class="text-body-2">Управление столами</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card class="text-center" color="error" dark @click="$router.push('/orders')">
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-receipt</v-icon>
            <div class="text-h6">Заказы</div>
            <div class="text-body-2">Управление заказами</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="text-center" color="purple" dark @click="$router.push('/positions')">
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-briefcase</v-icon>
            <div class="text-h6">Должности</div>
            <div class="text-body-2">Управление должностями</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup></script>

<style scoped>
.v-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}
</style>
