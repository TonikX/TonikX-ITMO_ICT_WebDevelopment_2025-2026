<template>
  <div class="not-found-view">
    <v-container class="fill-height">
      <v-row justify="center" align="center">
        <v-col cols="12" class="text-center">
          <div class="error-code">404</div>
          <h1 class="error-title mb-4">Страница не найдена</h1>
          <p class="text-medium-emphasis mb-6">
            К сожалению, запрашиваемая страница не существует или была удалена.
          </p>
          <v-btn color="primary" size="large" :to="{ name: 'home' }">
            <v-icon left>mdi-home</v-icon>
            На главную
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found-view {
  min-height: 60vh;
}

.error-code {
  font-family: 'Cormorant Garamond', serif;
  font-size: 8rem;
  font-weight: 700;
  color: #C9A959;
  line-height: 1;
  opacity: 0.8;
}

.error-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-background));
}
</style>

