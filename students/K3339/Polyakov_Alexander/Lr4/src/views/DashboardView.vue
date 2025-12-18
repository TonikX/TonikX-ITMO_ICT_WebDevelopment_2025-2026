<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const quickLinks = [
  {
    title: 'Manufacturers',
    subtitle: 'Keep producer info in sync across products.',
    to: '/catalog/manufacturers',
    icon: 'mdi-factory',
  },
  {
    title: 'Products',
    subtitle: 'Manage trade items, codes, units and shelf life.',
    to: '/catalog/products',
    icon: 'mdi-package-variant',
  },
  {
    title: 'Batches',
    subtitle: 'Create and track broker batches and contracts.',
    to: '/trading/batches',
    icon: 'mdi-truck-delivery',
  },
  {
    title: 'Batch Items',
    subtitle: 'Break batches down to products, pricing and expiry.',
    to: '/trading/batch-items',
    icon: 'mdi-cube-scan',
  },
  {
    title: 'Reports',
    subtitle: 'Analytics: volumes, revenue leaders, expired lots, salaries.',
    to: '/reports/latest-trades',
    icon: 'mdi-file-chart',
  },
]
</script>

<template>
  <v-container class="py-8 dashboard-wrapper" fluid>
    <v-row>
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="text-h5">Welcome to the Trading Desk</v-card-title>
          <v-card-text>
            Manage catalog data, create trading batches, and explore analytics from the reports
            section.
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <div class="card-grid">
      <div
        v-for="(link, idx) in quickLinks"
        :key="link.to"
        class="grid-item"
        :class="`area-${idx}`"
      >
        <v-card class="hover-card dashboard-card" height="220" @click="router.push(link.to)">
          <v-card-item>
            <div class="card-header">
              <v-icon :icon="link.icon" color="primary" size="30" class="mr-3" />
              <v-card-title class="text-h6 mb-1">{{ link.title }}</v-card-title>
            </div>
            <div class="card-subtitle text-body-2 text-medium-emphasis">
              {{ link.subtitle }}
            </div>
          </v-card-item>
        </v-card>
      </div>
    </div>
  </v-container>
</template>

<style scoped>
.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-grid {
  max-width: 1320px;
  margin: 24px auto 0;
  display: grid;
  grid-template-columns: repeat(6, minmax(120px, 1fr));
  column-gap: 28px;
  row-gap: 44px;
  justify-items: center;
  justify-content: center;
  width: 100%;
}

.area-0 { grid-column: 1 / span 2; grid-row: 1; }
.area-1 { grid-column: 3 / span 2; grid-row: 1; }
.area-2 { grid-column: 5 / span 2; grid-row: 1; }
.area-3 { grid-column: 2 / span 2; grid-row: 2; }
.area-4 { grid-column: 4 / span 2; grid-row: 2; }

.grid-item {
  width: 100%;
  display: flex;
  justify-content: center;
}

.hover-card {
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
  display: flex;
}

.dashboard-card {
  width: 100%;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: linear-gradient(145deg, #ffffff, #f3f6ff);
}
.hover-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 32px rgba(33, 150, 243, 0.22);
}

.card-header {
  display: flex;
  align-items: center;
}

.card-subtitle {
  margin-top: 8px;
  line-height: 1.4;
}
</style>

