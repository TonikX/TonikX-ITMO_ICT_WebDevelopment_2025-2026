import { onMounted, ref } from "vue";
import { getChickens } from "@/api/chickens.js";
import { getLastEggProduction } from "@/api/eggProductionMonth.js";
import { getAgeFromDate } from "@/utils/age.js";

export function useChickens() {
  const chickens = ref([]);
  const loading = ref(true);

  const fetchChickens = async () => {
    loading.value = true;
    try {
      const baseChickens = await getChickens();

      chickens.value = await Promise.all(
        baseChickens.map(async (chicken) => {
          const eggs = await getLastEggProduction(chicken.id);
          return {
            ...chicken,
            age: getAgeFromDate(chicken.birthDate),
            eggs,
            breedId: chicken.breed?.id,
            breedName: chicken.breed?.name
          };
        })
      );
    } catch (e) {
      console.error("Ошибка при получении данных:", e);
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchChickens);

  return { chickens, loading, fetchChickens };
}