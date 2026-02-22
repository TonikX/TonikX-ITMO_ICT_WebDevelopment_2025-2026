<template>
  <v-footer class="bg-background mt-10" border>
    <v-container>
      <v-row>
        <v-col cols="12" md="4">
          <div class="text-h6 font-weight-bold mb-4">
            <span class="text-primary">Brand</span>
            <span class="text-secondary">Pro</span>
          </div>
          <p class="text-body-2 text-grey">
            Развиваем ваш личный бренд с помощью профессиональных услуг
          </p>
        </v-col>

        <v-col cols="6" md="2">
          <div class="text-subtitle-1 font-weight-bold mb-3">Навигация</div>
          <v-list density="compact" class="bg-transparent">
            <v-list-item to="/" title="Главная" />
            <v-list-item to="/services" title="Услуги" />
          </v-list>
        </v-col>

        <v-col cols="6" md="2">
          <div class="text-subtitle-1 font-weight-bold mb-3">Аккаунт</div>
          <v-list density="compact" class="bg-transparent">
            <v-list-item to="/login" title="Войти" />
            <v-list-item to="/register" title="Регистрация" />
          </v-list>
        </v-col>

        <v-col cols="12" md="4" class="text-right">
          <div class="text-subtitle-1 font-weight-bold mb-3">Контакты</div>
          <p class="text-body-2 text-grey mb-1">
            <v-icon icon="mdi-email" size="small" class="mr-2"></v-icon>
            contact@brandpro.ru
          </p>
          <p class="text-body-2 text-grey">
            <v-icon icon="mdi-phone" size="small" class="mr-2"></v-icon>
            +7 (999) 123-45-67
          </p>
        </v-col>
      </v-row>

      <v-divider class="my-4"></v-divider>

      <v-row align="center" justify="center">
        <v-col cols="12" class="text-center text-body-2 text-grey">
          © {{ new Date().getFullYear() }} BrandPro. Все права защищены.
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup>
</script>