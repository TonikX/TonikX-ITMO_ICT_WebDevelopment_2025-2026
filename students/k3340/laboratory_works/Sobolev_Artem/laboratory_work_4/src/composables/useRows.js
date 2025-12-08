import { ref, onMounted } from "vue";
import http from "@/api/http.js";
import { getWorkshops } from "@/api/workshops.js";

export default function useRows() {
  const rows = ref([]);
  const loading = ref(true);

  const fetchRows = async () => {
    loading.value = true;
    try {
      const workshops = await getWorkshops();

      const allRows = await Promise.all(
        workshops.map(async (workshop) => {
          try {
            const { data } = await http.get(`/api/v1/workshops/${workshop.id}/rows`);
            return data.payload || [];
          } catch (err) {
            console.error(`Ошибка при получении рядов для цеха ${workshop.id}:`, err);
            return [];
          }
        })
      );

      rows.value = allRows.flat();
    } catch (e) {
      console.error("Ошибка при загрузке рядов:", e);
      rows.value = [];
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchRows);

  return { rows, loading, fetchRows };
}
