<template>
  <div class="chicken-page">
    <Loader v-if="loading" />

    <div v-else-if="chicken" class="chicken-content">
      <div class="chicken-card">
        <h2 class="chicken-name">{{ chicken.name }}</h2>

        <div class="chicken-details">
          <div class="detail-row">
            <span class="detail-label">ID:</span>
            <span class="detail-value">{{ chicken.id }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Вес:</span>
            <span class="detail-value">{{ chicken.weight }} г</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Дата рождения:</span>
            <span class="detail-value">{{ formattedBirthDate }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Возраст:</span>
            <span class="detail-value">{{ age }}</span>
          </div>
        </div>
      </div>

      <div v-if="chicken.breed" class="breed-card">
        <h3 class="card-title">Порода</h3>

        <div class="breed-details">
          <div class="detail-row">
            <span class="detail-label">Название:</span>
            <span class="detail-value">{{ chicken.breed.name }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">ID породы:</span>
            <span class="detail-value">{{ chicken.breed.id }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Яйценоскость:</span>
            <span class="detail-value">{{ chicken.breed.eggsNumber }} яиц/год</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Стандартный вес:</span>
            <span class="detail-value">{{ chicken.breed.weight }} г</span>
          </div>
        </div>
      </div>

      <div v-if="chicken.cage" class="cage-card">
        <h3 class="card-title">Клетка</h3>

        <div class="cage-details">
          <div class="detail-row">
            <span class="detail-label">ID клетки:</span>
            <span class="detail-value">{{ chicken.cage.id }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Номер клетки:</span>
            <span class="detail-value">{{ chicken.cage.cageNumber }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">ID ряда:</span>
            <span class="detail-value">{{ chicken.cage.rowId }}</span>
          </div>
        </div>
      </div>
    </div>

    <p v-else class="error">Курица не найдена</p>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import Loader from "@/components/ui/Loader.vue";
import { getChicken } from "@/api/chickens.js";
import { getAgeFromDate } from "@/utils/age.js";
import { formatDate } from "@/utils/formatDate.js";

const route = useRoute();
const chickenId = Number(route.params.id);

const chicken = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchChicken = async () => {
  loading.value = true;
  try {
    const data = await getChicken(chickenId);
    if (data) {
      chicken.value = data;
    } else {
      error.value = "Курица не найдена";
    }
  } catch (e) {
    console.error("Ошибка при получении данных о курице:", e);
    error.value = "Ошибка при загрузке данных";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchChicken);

const age = computed(() => {
  if (!chicken.value?.birthDate) return "";
  return getAgeFromDate(chicken.value.birthDate);
});

const formattedBirthDate = computed(() => {
  if (!chicken.value?.birthDate) return "";
  return formatDate(chicken.value.birthDate);
});
</script>

<style scoped lang="scss">
.chicken-page {
  min-height: 60vh;
}

.chicken-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 600px;
  margin: 0 auto;
}

.chicken-card,
.breed-card,
.cage-card {
  background: var(--section-bg);
  border-radius: 8px;
  padding: 24px;
  border: 1px solid var(--sidebar-text);
}

.chicken-name {
  margin: 0 0 20px 0;
  color: var(--color);
  font-size: 24px;
  font-weight: 600;
}

.card-title {
  margin: 0 0 16px 0;
  color: var(--color);
  font-size: 18px;
  font-weight: 600;
}

.chicken-details,
.breed-details,
.cage-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
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
}

.detail-value {
  color: var(--color);
  font-weight: 400;
}

.error {
  text-align: center;
  color: var(--error-color);
  padding: 40px;
  font-size: 18px;
}
</style>