<template>
  <div class="admin-copy-transfer">
    <v-container>
      <v-row>
        <v-col cols="12">
          <div class="d-flex align-center mb-4">
            <v-btn
              icon="mdi-arrow-left"
              variant="text"
              @click="$router.push('/admin/books')"
              class="mr-2"
            ></v-btn>
            <h1 class="text-h4">Перемещение экземпляра книги</h1>
          </div>

          <v-card>
            <v-card-text>
              <p class="text-body-1">Форма перемещения экземпляра в разработке.</p>
              <p>Здесь можно будет указать ID экземпляра и новый зал.</p>

              <v-alert type="info" variant="tonal" class="mt-4">
                ⚡ Для перемещения экземпляра используйте админ-панель Django
              </v-alert>

              <v-btn
                color="primary"
                href="http://127.0.0.1:8000/admin/library_app/copyofbook/"
                target="_blank"
              >
                Перейти в админку Django
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>