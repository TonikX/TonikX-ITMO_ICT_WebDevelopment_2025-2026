<template>
  <div class="reports-page">
    <h1 class="page-title">Отчет по разнице яйценоскости пород</h1>

    <div v-if="report && !loading" class="summary-section">
      <h2 class="section-title">Статистика за {{ monthFormatted }} {{ report.year }}</h2>

      <div class="summary-cards">
        <div class="summary-card">
          <div class="card-title">Всего пород</div>
          <div class="card-value">{{ report.length || 0 }}</div>
        </div>

        <div class="summary-card">
          <div class="card-title">Средняя разница</div>
          <div class="card-value">{{ avgDifferenceFormatted }}</div>
        </div>

        <div class="summary-card">
          <div class="card-title">Лучшая порода</div>
          <div class="card-value">{{ bestBreedName || 'Нет данных' }}</div>
        </div>

        <div class="summary-card">
          <div class="card-title">Средняя по ферме</div>
          <div class="card-value">{{ farmAvgEggsFormatted }}</div>
        </div>
      </div>
    </div>

    <div v-if="report && !loading && report.length > 0" class="table-section">
      <h2 class="section-title">Детальная статистика по породам</h2>

      <EggDiffTable
          :headers-item="[
            { key: 'breedName', label: 'Порода' },
            { key: 'breedAvgEggs', label: 'Средняя яйценоскость породы' },
            { key: 'farmAvgEggs', label: 'Средняя по ферме' },
            { key: 'diffEggs', label: 'Разница' },
            { key: 'performance', label: 'Производительность' }
          ]"
          :body-items="report"
          :height-size="report.length"
      />
    </div>

    <div v-else-if="report && !loading && report.length === 0" class="no-data">
      <p>Нет данных для отображения за указанный период</p>
    </div>

    <Loader v-if="loading"/>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import Loader from "@/components/ui/Loader.vue";
import EggDiffTable from "@/components/tables/ReportBreedEggDifferenceTable.vue";
import { getBreedEggDiffReport } from "@/api/reports.js";

const month = ref(new Date().getMonth() + 1);
const year = ref(new Date().getFullYear());
const report = ref(null);
const loading = ref(false);
const error = ref("");

const monthFormatted = computed(() => {
  const months = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];
  return months[month.value - 1] || '';
});

const avgDifference = computed(() => {
  if (!report.value || report.value.length === 0) return 0;

  const sum = report.value.reduce((total, breed) => total + (breed.diffEggs || 0), 0);
  return sum / report.value.length;
});

const avgDifferenceFormatted = computed(() => {
  return `${avgDifference.value.toFixed(1)} яиц`;
});

const farmAvgEggsFormatted = computed(() => {
  if (!report.value || report.value.length === 0) return 'Нет данных';
  const firstBreed = report.value[0];
  return `${firstBreed.farmAvgEggs?.toFixed(1) || 0} яиц`;
});

const bestBreedName = computed(() => {
  if (!report.value || report.value.length === 0) return '';

  const breedsWithPositiveDiff = report.value.filter(breed => breed.diffEggs > 0);
  if (breedsWithPositiveDiff.length === 0) return 'Нет положительных значений';

  const bestBreed = breedsWithPositiveDiff.reduce((best, current) =>
      current.diffEggs > best.diffEggs ? current : best
  );

  return bestBreed.breedName;
});

const fetchReport = async () => {
  if (!month.value || !year.value) {
    error.value = "Пожалуйста, введите месяц и год";
    return;
  }

  if (month.value < 1 || month.value > 12) {
    error.value = "Месяц должен быть от 1 до 12";
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const data = await getBreedEggDiffReport(year.value, month.value);
    report.value = data;
  } catch (e) {
    console.error("Ошибка при получении отчета:", e);
    error.value = "Ошибка при загрузке отчета. Проверьте введенные данные.";
    report.value = null;
  } finally {
    loading.value = false;
  }
};

onMounted(fetchReport);
</script>

<style scoped lang="scss">
.reports-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  color: var(--color);
  font-size: 28px;
  margin-bottom: 32px;
  text-align: center;
}

.add-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: var(--section-bg);
  border-radius: 8px;
  padding: 24px;
  border: 1px solid var(--sidebar-text);
  margin-bottom: 32px;
}

.form-header {
  margin-bottom: 8px;
}

.form-title {
  font-weight: 600;
  font-size: 20px;
  color: var(--color);
  margin: 0;
}

.form-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  gap: 32px;
}

.add-form__label {
  display: flex;
  flex-direction: column;
}

.add-form__label-title {
  font-weight: 500;
  margin-bottom: 4px;
  color: var(--color);
}

.add-form__input {
  padding: 8px;
  border: 1px solid var(--sidebar-text);
  border-radius: 4px;
  background: var(--section-bg);
  color: var(--color);
  font-size: 16px;

  &:focus {
    outline: none;
    border-color: var(--violet);
  }
}

.error-message {
  color: var(--error-color);
  text-align: center;
  padding: 8px;
  margin-top: 8px;
  background: rgba(244, 67, 54, 0.1);
  border-radius: 4px;
}

.summary-section {
  margin-bottom: 32px;
}

.section-title {
  font-weight: 600;
  font-size: 20px;
  color: var(--color);
  margin-bottom: 20px;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.summary-card {
  background: var(--section-bg);
  border-radius: 8px;
  padding: 20px;
  border: 1px solid var(--sidebar-text);
  text-align: center;
}

.card-title {
  color: var(--sidebar-text);
  font-size: 14px;
  margin-bottom: 8px;
  font-weight: 500;
}

.card-value {
  color: var(--color);
  font-size: 20px;
  font-weight: 600;
  word-break: break-word;
}

.table-section {
  background: var(--section-bg);
  border-radius: 8px;
  padding: 24px;
  border: 1px solid var(--sidebar-text);
}

.no-data {
  text-align: center;
  color: var(--sidebar-text);
  padding: 40px;
  background: var(--section-bg);
  border-radius: 8px;
  border: 1px solid var(--sidebar-text);
  font-style: italic;
}
</style>