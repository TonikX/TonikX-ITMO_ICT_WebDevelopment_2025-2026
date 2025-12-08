import { ref, onMounted } from "vue";
import http from "@/api/http.js";

export default function useWorkshops() {
  const workshops = ref([]);
  const loading = ref(true);

  const fetchWorkshops = async () => {
    loading.value = true;
    try {
      const { data } = await http.get("/api/v1/workshops");
      workshops.value = data.payload || [];
    } catch (e) {
      console.error("Ошибка при получении данных о цехах:", e);
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchWorkshops);

  return { workshops, loading, fetchWorkshops };
}
