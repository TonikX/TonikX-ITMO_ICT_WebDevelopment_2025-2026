import { ref, onMounted } from "vue";
import http from "@/api/http.js";
import { getChickens } from "@/api/chickens.js";

export default function useEggProductions() {
  const eggProductions = ref([]);
  const loading = ref(true);

  const fetchEggProductions = async () => {
    loading.value = true;
    try {
      const chickens = await getChickens();

      const allProductions = await Promise.all(
        chickens.map(async (chicken) => {
          try {
            const { data } = await http.get(`/api/v1/chickens/${chicken.id}/egg-productions`);
            const productions = data.payload || [];

            return productions.map(production => ({
              ...production,
              chickenName: production.chicken?.name || chicken.name,
              breedName: production.chicken?.breed?.name || chicken.breed?.name || 'Не указана'
            }));
          } catch (err) {
            console.error(`Ошибка при получении производства для курицы ${chicken.id}:`, err);
            return [];
          }
        })
      );

      eggProductions.value = allProductions.flat();
    } catch (e) {
      console.error("Ошибка при загрузке производства яиц:", e);
      eggProductions.value = [];
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchEggProductions);

  return { eggProductions, loading, fetchEggProductions };
}