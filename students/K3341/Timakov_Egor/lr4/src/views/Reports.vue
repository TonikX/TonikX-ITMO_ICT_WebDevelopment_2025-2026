<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span class="text-h5">Отчёты</span>
            <v-btn color="primary" @click="openDialog">
              <v-icon start>mdi-plus</v-icon>
              Создать отчёт
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-select
                v-model="typeFilter"
                :items="reportTypes"
                item-title="title"
                item-value="value"
                label="Фильтр по типу"
                variant="outlined"
                class="mb-4"
                @change="loadReports"
                clearable
            ></v-select>

            <v-data-table
                :headers="headers"
                :items="reports"
                :loading="loading"
                no-data-text="Нет данных."
                item-key="id"
            >
              <template v-slot:item.report_type_display="{ item }">
                <v-chip>{{ item.report_type_display }}</v-chip>
              </template>
              <template v-slot:item.created_by_name="{ item }">
                {{ item.created_by_name }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn icon="mdi-eye" size="small" @click="viewReport(item)"></v-btn>
                <v-btn icon="mdi-delete" size="small" color="error" @click="deleteReport(item)"></v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог создания отчёта -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>Создать отчёт</v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="createReport">
            <v-text-field
                v-model="form.title"
                label="Название отчёта"
                variant="outlined"
                required
            ></v-text-field>
            <v-select
                v-model="form.report_type"
                :items="reportTypes"
                item-title="title"
                item-value="value"
                label="Тип отчёта"
                variant="outlined"
                required
            ></v-select>
            <v-text-field
                v-model="form.start_date"
                label="Начальная дата"
                type="date"
                variant="outlined"
            ></v-text-field>
            <v-text-field
                v-model="form.end_date"
                label="Конечная дата"
                type="date"
                variant="outlined"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" type="submit" @click="createReport">
            Создать
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, reactive, onMounted } from "vue";
import { reportsApi, employeesApi } from "../services/api";

export default {
  name: "Reports",
  setup() {
    const reports = ref([]); // Список отчётов
    const typeFilter = ref(""); // Фильтр по типу отчёта
    const loading = ref(false); // Отображение состояния загрузки
    const dialog = ref(false); // Управляет состоянием модального окна
    const currentUser = ref(null); // Данные текущего сотрудника
    const form = reactive({
      title: "",
      report_type: "",
      start_date: "",
      end_date: "",
      created_by: null, // ID текущего сотрудника
    });

    const reportTypes = [
      { title: "Финансовый отчёт", value: "financial" },
      { title: "Отчёт по книгам", value: "books" },
      { title: "Отчёт по сотрудникам", value: "employees" },
      { title: "Отчёт по продажам", value: "sales" },
      { title: "Пользовательский отчёт", value: "custom" },
    ];

    const headers = [
      { title: "Название", key: "title" },
      { title: "Тип", key: "report_type_display" },
      { title: "Период", key: "start_date" },
      { title: "Действия", key: "actions", sortable: false },
    ];

    const loadReports = async () => {
      loading.value = true;
      try {
        const params = typeFilter.value ? { type: typeFilter.value } : {};
        const response = await reportsApi.getAll(params);
        reports.value = response.data.results || response.data; // Загружаем список отчётов
      } catch (error) {
        console.error("Ошибка загрузки отчётов:", error);
      } finally {
        loading.value = false;
      }
    };

    const loadCurrentUser = async () => {
      try {
        const response = await employeesApi.getAll(); // Предположим, возвращает текущего пользователя
        currentUser.value = response.data.results?.[0] || response.data[0]; // Предполагаем, что первый результат - текущий пользователь
        form.created_by = currentUser.value.id; // Присваиваем ID текущего пользователя
      } catch (error) {
        console.error("Ошибка загрузки текущего пользователя:", error);
      }
    };

    const openDialog = () => {
      form.title = "";
      form.report_type = "";
      form.start_date = "";
      form.end_date = "";
      form.created_by = currentUser.value?.id || null; // Убедитесь, что ID текущего сотрудника передан
      dialog.value = true;
    };

    const closeDialog = () => {
      dialog.value = false;
    };

    const createReport = async () => {
      if (!form.title || !form.report_type || !form.created_by) {
        alert("Пожалуйста, заполните все обязательные поля.");
        return;
      }

      try {
        console.log("Отправка данных:", form);
        await reportsApi.create(form);
        dialog.value = false;
        loadReports();
      } catch (error) {
        console.error("Ошибка создания отчёта:", error);
        alert("Не удалось создать отчёт. Проверьте данные и повторите попытку.");
      }
    };

    onMounted(async () => {
      await loadCurrentUser(); // Загружаем текущего пользователя
      await loadReports(); // Загружаем отчёты
    });

    return {
      reports,
      form,
      dialog,
      typeFilter,
      headers,
      reportTypes,
      loading,
      openDialog,
      closeDialog,
      createReport,
      loadReports,
    };
  },
};
</script>