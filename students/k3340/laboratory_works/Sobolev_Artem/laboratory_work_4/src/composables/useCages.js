import { ref, onMounted } from "vue";
import http from "@/api/http.js";
import { getWorkshops } from "@/api/workshops.js";

export default function useCages() {
  const cages = ref([]);
  const loading = ref(true);

  const fetchCages = async () => {
    loading.value = true;
    try {
      const workshops = await getWorkshops();

      const allCages = await Promise.all(
        workshops.map(async (workshop) => {
          try {
            const { data: rowsData } = await http.get(`/api/v1/workshops/${workshop.id}/rows`);
            const rows = rowsData.payload || [];

            const cagesPromises = rows.map(async (row) => {
              try {
                const { data: cagesData } = await http.get(`/api/v1/rows/${row.id}/cage`);
                const cages = cagesData.payload || [];

                return cages.map(cage => ({
                  ...cage,
                  workshopId: workshop.id
                }));
              } catch (cageErr) {
                console.error(`Ошибка при получении клеток для ряда ${row.id}:`, cageErr);
                return [];
              }
            });

            const cagesResults = await Promise.all(cagesPromises);
            return cagesResults.flat();
          } catch (rowErr) {
            console.error(`Ошибка при получении рядов для цеха ${workshop.id}:`, rowErr);
            return [];
          }
        })
      );

      cages.value = allCages.flat();
    } catch (e) {
      console.error("Ошибка при загрузке клеток:", e);
      cages.value = [];
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchCages);

  return { cages, loading, fetchCages };
}