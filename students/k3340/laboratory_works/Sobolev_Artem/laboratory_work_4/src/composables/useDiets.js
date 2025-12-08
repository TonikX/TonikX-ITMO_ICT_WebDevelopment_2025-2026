import { onMounted, ref } from "vue";
import { getDiets } from "@/api/diets.js";

export default function useDiets() {
  const diets = ref([]);
  const loading = ref(true);

  const fetchDiets = async () => {
    loading.value = true;
    try {
      diets.value = await getDiets();
    } catch (e) {
      console.error("Ошибка при получении данных:", e);
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchDiets);

  return { diets, loading, fetchDiets };
}
