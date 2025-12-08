<template>
  <div class="worker-page">
    <Loader v-if="loading" />

    <div v-else-if="worker" class="worker-content">
      <div class="worker-card">
        <h2 class="worker-name">
          {{ worker.lastName }} {{ worker.firstName }} {{ worker.patronymic }}
        </h2>

        <div class="worker-details">
          <div class="detail-row">
            <span class="detail-label">ID:</span>
            <span class="detail-value">{{ worker.id }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Фамилия:</span>
            <span class="detail-value">{{ worker.lastName }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Имя:</span>
            <span class="detail-value">{{ worker.firstName }}</span>
          </div>

          <div v-if="worker.patronymic" class="detail-row">
            <span class="detail-label">Отчество:</span>
            <span class="detail-value">{{ worker.patronymic }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Телефон:</span>
            <span class="detail-value">{{ worker.phoneNumber }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Email:</span>
            <span class="detail-value">{{ worker.email }}</span>
          </div>
        </div>
      </div>

      <div v-if="worker.cages && worker.cages.length > 0" class="cages-card">
        <h3 class="card-title">Закрепленные клетки</h3>

        <div class="cages-list">
          <div v-for="cage in worker.cages" :key="cage.id" class="cage-item">
            <div class="cage-details">
              <div class="detail-row">
                <span class="detail-label">ID клетки:</span>
                <span class="detail-value">{{ cage.id }}</span>
              </div>

              <div class="detail-row">
                <span class="detail-label">Номер клетки:</span>
                <span class="detail-value">{{ cage.cageNumber }}</span>
              </div>

              <div class="detail-row">
                <span class="detail-label">ID ряда:</span>
                <span class="detail-value">{{ cage.rowId }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="cages-card">
        <h3 class="card-title">Закрепленные клетки</h3>
        <p class="no-cages">За работником не закреплено клеток</p>
      </div>
    </div>

    <p v-else class="error">Работник не найден</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import Loader from "@/components/ui/Loader.vue";
import { getWorker, getWorkerContract } from "@/api/workers.js";

const route = useRoute();
const router = useRouter();
const workerId = Number(route.params.id);

const worker = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchWorker = async () => {
  loading.value = true;
  try {
    const data = await getWorker(workerId);
    if (data) {
      worker.value = data;
    } else {
      error.value = "Работник не найден";
    }
  } catch (e) {
    console.error("Ошибка при получении данных о работнике:", e);
    error.value = "Ошибка при загрузке данных";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchWorker);
</script>

<style scoped lang="scss">
.worker-page {
  min-height: 60vh;
  padding: 20px;
}

.worker-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.worker-card,
.cages-card,
.actions-card {
  background: var(--section-bg);
  border-radius: 8px;
  padding: 24px;
  border: 1px solid var(--sidebar-text);
}

.worker-name {
  margin: 0 0 20px 0;
  color: var(--color);
  font-size: 24px;
  font-weight: 600;
  text-align: center;
}

.card-title {
  margin: 0 0 20px 0;
  color: var(--color);
  font-size: 18px;
  font-weight: 600;
  border-bottom: 2px solid var(--violet);
  padding-bottom: 8px;
}

.worker-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cages-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cage-item {
  background: var(--background);
  border-radius: 6px;
  border: 1px solid var(--sidebar-border);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--sidebar-border);

  &:last-child {
    border-bottom: none;
  }
}

.detail-label {
  color: var(--sidebar-text);
  font-weight: 500;
  min-width: 120px;
}

.detail-value {
  color: var(--color);
  font-weight: 400;
  text-align: right;
  word-break: break-word;
}

.no-cages {
  color: var(--sidebar-text);
  text-align: center;
  font-style: italic;
  padding: 20px 0;
}

.actions-buttons {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: center;

  @media (max-width: 600px) {
    flex-direction: column;
    align-items: center;
  }
}

.error {
  text-align: center;
  color: var(--error-color);
  padding: 40px;
  font-size: 18px;
}

/* Стили для кнопок */
.block-action {
  font-weight: 600;
  font-size: 14px;
  min-width: 200px;
  border-radius: 8px;
  padding-block: 12px;
}

.violet {
  background-color: var(--contrast);
  color: var(--color-white);
}

.violet-no-switch {
  background-color: var(--color-section-contrast-light);
  color: var(--color-white);
}
</style>