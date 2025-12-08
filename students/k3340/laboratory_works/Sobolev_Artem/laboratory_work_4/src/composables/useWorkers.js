import {onMounted, ref} from "vue";
import {getWorker, getWorkerContract, getWorkers} from "@/api/workers.js";

export function useWorkers() {
  const workers = ref([]);
  const loading = ref(true);

  onMounted(async () => {
    try {
      const baseWorkers = await getWorkers();
      workers.value = await Promise.all(
        baseWorkers.map(async (worker) => {
          const contract = await getWorkerContract(worker.id);
          const fullWorker = await getWorker(worker.id);
          return {
            ...worker,
            position: contract?.position || "-",
            salary: contract?.salary || "-",
            workersCells: fullWorker?.cages?.map(c => c.cageNumber).join(", ") || "-"
          };
        })
      );
    } catch (e) {
      console.error("Ошибка при получении данных:", e);
    } finally {
      loading.value = false;
    }
  });

  return { workers, loading };
}