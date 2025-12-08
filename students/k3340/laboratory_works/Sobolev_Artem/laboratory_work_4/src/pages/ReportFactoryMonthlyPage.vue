<template>
  <div class="reports-page">
    <h1 class="page-title">Ежемесячный отчет по производству</h1>

    <form @submit.prevent="fetchReport" class="add-form">
      <div class="form-header">
        <h2 class="form-title">Параметры отчета</h2>
      </div>
      <div class="form-wrapper">
        <label class="add-form__label">
          <span class="add-form__label-title">Месяц:</span>
          <input
              class="add-form__input"
              type="number"
              min="1"
              max="12"
              v-model="month"
              placeholder="Введите месяц (1-12)"
              required
          />
        </label>

        <label class="add-form__label">
          <span class="add-form__label-title">Год:</span>
          <input
              class="add-form__input"
              type="number"
              min="2000"
              max="2100"
              v-model="year"
              placeholder="Введите год (YYYY)"
              required
          />
        </label>

        <Button
            label="Сформировать отчет"
            mode="violet"
            location="report-form"
            type="submit"
            style="align-self: center; margin-top: 40px;"
            :loading="loading"
        />
      </div>




      <p v-if="error" class="error-message">{{ error }}</p>
    </form>

    <div v-if="report && !loading" class="summary-section">
      <h2 class="section-title">Общая статистика за {{ monthFormatted }} {{ report.year }}</h2>

      <div class="summary-cards">
        <div class="summary-card">
          <div class="card-title">Всего куриц</div>
          <div class="card-value">{{ report.totalChickens }}</div>
        </div>

        <div class="summary-card">
          <div class="card-title">Всего яиц</div>
          <div class="card-value">{{ report.totalEggs }}</div>
        </div>

        <div class="summary-card">
          <div class="card-title">Средняя яйценоскость</div>
          <div class="card-value">{{ avgEggsPerChickenTotal }} яиц/курицу</div>
        </div>
      </div>
    </div>

    <div v-if="report && !loading && report.stats && report.stats.length > 0" class="table-section">
      <h2 class="section-title">Детальная статистика по цехам</h2>

      <ReportFactoryMonthlyTable
          :headers-item="[
            { key: 'workshopNumber', label: 'Номер цеха' },
            { key: 'breedName', label: 'Порода' },
            { key: 'chickensCount', label: 'Количество куриц' },
            { key: 'eggsTotal', label: 'Всего яиц' },
            { key: 'avgEggsPerChicken', label: 'Средняя яйценоскость' }
          ]"
          :body-items="report.stats"
          :height-size="report.stats.length"
      />
    </div>

    <div v-else-if="report && !loading && (!report.stats || report.stats.length === 0)" class="no-data">
      <p>Нет данных для отображения за указанный период</p>
    </div>

    <Loader v-if="loading"/>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import Button from "@/components/ui/Button.vue";
import Loader from "@/components/ui/Loader.vue";
import ReportFactoryMonthlyTable from "@/components/tables/ReportFactoryMonthlyTable.vue";
import { getMonthlyFactoryReport } from "@/api/reports.js";

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

const avgEggsPerChickenTotal = computed(() => {
  if (!report.value || !report.value.totalChickens || report.value.totalChickens === 0) {
    return 0;
  }
  return (report.value.totalEggs / report.value.totalChickens).toFixed(1);
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
    const data = await getMonthlyFactoryReport(year.value, month.value);
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
  align-items: flex-end;
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
  font-size: 24px;
  font-weight: 600;
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