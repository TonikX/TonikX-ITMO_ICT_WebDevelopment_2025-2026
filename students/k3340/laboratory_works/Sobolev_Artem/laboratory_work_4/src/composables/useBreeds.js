import {onMounted, ref} from "vue";
import {getBreeds} from "@/api/breeds.js";

export default function useBreeds() {
  const breeds = ref([]);
  const loading = ref(true);

  const fetchBreeds = async () => {
    loading.value = true;
    try {
      breeds.value = await getBreeds();
    } catch (e) {
      console.error("Ошибка при получении данных:", e);
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchBreeds);

  return { breeds, loading, fetchBreeds };
}