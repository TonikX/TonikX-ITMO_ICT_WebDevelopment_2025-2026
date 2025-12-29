<template>
  <v-row class="mb-6">
    <v-col cols="12">
      <v-card class="pa-6">
        <v-row>
          <v-col cols="12" md="3" class="text-center">
            <v-avatar size="200" class="mb-4">
              <v-img
                  v-if="company.logo && isValidLogo(company.logo)"
                  :src="company.logo"
                  cover
                  class="company-logo"
              >
                <template v-slot:placeholder>
                  <v-icon size="100" color="grey-lighten-1">mdi-office-building</v-icon>
                </template>
              </v-img>
              <div v-else class="no-logo-detail">
                <v-icon size="100" color="grey-lighten-1">mdi-office-building</v-icon>
                <div class="text-caption mt-2">Нет логотипа</div>
              </div>
            </v-avatar>
          </v-col>

          <v-col cols="12" md="9">
            <div class="d-flex align-center mb-4">
              <h1 class="text-h4">{{ company.name }}</h1>
              <v-spacer></v-spacer>
              <v-btn
                  v-if="isCompanyOwner"
                  to="/company"
                  color="primary"
                  variant="outlined"
              >
                Управлять
              </v-btn>
            </div>

            <div class="mb-4">
              <v-chip
                  v-if="company.average_rating"
                  color="amber"
                  text-color="white"
                  size="large"
                  class="mr-2"
              >
                <v-icon start icon="mdi-star"></v-icon>
                {{ company.average_rating.toFixed(1) }}
                <span class="ml-1">({{ company.reviews?.length || 0 }})</span>
              </v-chip>

              <v-chip
                  color="primary"
                  variant="outlined"
                  size="large"
                  class="mr-2"
              >
                <v-icon start icon="mdi-tools"></v-icon>
                {{ company.services?.length || 0 }} услуг
              </v-chip>

              <v-chip
                  v-if="company.user"
                  color="secondary"
                  variant="outlined"
                  size="large"
              >
                <v-icon start icon="mdi-account"></v-icon>
                {{ company.user.name }} {{ company.user.surname }}
              </v-chip>
            </div>

            <p class="text-body-1 mb-4">
              {{ company.description || 'Нет описания' }}
            </p>

            <div v-if="company.website && company.website !== 'https://example.com'" class="mb-2">
              <v-icon icon="mdi-web" class="mr-2"></v-icon>
              <a :href="company.website" target="_blank" class="text-body-1">
                {{ company.website }}
              </a>
            </div>

            <div class="text-caption text-grey">
              Владелец: {{ company.user?.email }}
            </div>
          </v-col>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  company: {
    type: Object,
    required: true
  },
  isCompanyOwner: {
    type: Boolean,
    default: false
  }
})

const isValidLogo = (logoUrl) => {
  if (!logoUrl || typeof logoUrl !== 'string') return false

  const invalidPatterns = [
    'via.placeholder.com',
    'example.com',
    'string',
    'test',
    'localhost',
    'placeholder.com'
  ]

  const lowerUrl = logoUrl.toLowerCase()
  return !invalidPatterns.some(pattern => lowerUrl.includes(pattern))
}
</script>

<style scoped>
.no-logo-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  color: #9e9e9e;
}

/* Адаптивные стили */
@media (max-width: 600px) {
  .company-image-container {
    height: 150px;
  }
}
</style>