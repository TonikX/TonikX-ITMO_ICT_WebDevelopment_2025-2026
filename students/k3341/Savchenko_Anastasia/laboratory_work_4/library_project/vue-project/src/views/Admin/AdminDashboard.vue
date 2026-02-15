<template>
  <div class="admin-dashboard">
    <v-container>
      <!-- Заголовок страницы -->
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-4">📊 Панель администратора</h1>
        </v-col>
      </v-row>

      <!-- Основные разделы (4 карточки) -->
      <v-row>
        <!-- Читатели -->
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title>👥 Читатели</v-card-title>
            <v-card-text>
              <p>Управление читателями</p>
              <v-btn color="primary" @click="$router.push('/admin/readers')">Перейти</v-btn>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Выдача книг -->
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title>📕 Выдача книг</v-card-title>
            <v-card-text>
              <p>Выдача книг читателям</p>
              <v-btn color="success" @click="$router.push('/admin/issue-book')">Выдать</v-btn>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Книги -->
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title>📚 Книги</v-card-title>
            <v-card-text>
              <p>Управление книгами</p>
              <v-btn color="primary" @click="$router.push('/admin/books')">Перейти</v-btn>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Отчеты -->
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title>📊 Отчеты</v-card-title>
            <v-card-text>
              <p>Статистика</p>
              <v-btn color="primary" @click="$router.push('/admin/reports')">Перейти</v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Быстрые действия (частые операции) -->
      <v-row class="mt-4">
        <v-col cols="12">
          <v-card>
            <v-card-title>⚡ Быстрые действия</v-card-title>
            <v-card-text>
              <v-btn color="success" class="mr-2" @click="$router.push('/admin/issue-book')">
                <v-icon left>mdi-book-plus</v-icon> Выдать
              </v-btn>
              <v-btn color="primary" class="mr-2" @click="$router.push('/admin/readers/register')">
                <v-icon left>mdi-account-plus</v-icon> Регистрация
              </v-btn>
              <v-btn color="info" class="mr-2" @click="$router.push('/admin/books/add')">
                <v-icon left>mdi-book-plus</v-icon> Добавить
              </v-btn>
              <v-btn color="warning" @click="$router.push('/admin/books/decommission')">
                <v-icon left>mdi-book-remove</v-icon> Списать
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

// Хук для навигации
const router = useRouter()
// Все переходы делаются через $router.push в шаблоне
</script>