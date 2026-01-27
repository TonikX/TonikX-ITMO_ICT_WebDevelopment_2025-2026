<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" md="6" class="text-center">
        <v-icon size="128" color="grey" class="mb-4">mdi-alert-circle</v-icon>
        <h1 class="text-h2 mb-4">404</h1>
        <p class="text-h5 mb-6">Страница не найдена</p>
        <p class="text-body-1 text-grey mb-8">
          Запрашиваемая страница не существует или была перемещена.
        </p>
        <v-btn color="primary" size="large" to="/">
          <v-icon left>mdi-home</v-icon>
          На главную
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>