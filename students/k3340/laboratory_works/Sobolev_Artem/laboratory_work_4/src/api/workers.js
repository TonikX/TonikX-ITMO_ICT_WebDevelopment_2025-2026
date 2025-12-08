import http from "@/api/http.js";

export async function getWorkers() {
  const { data } = await http.get("/api/v1/workers");
  return data.payload || [];
}

export async function getWorkerContract(id) {
  try {
    const { data } = await http.get(`/api/v1/workers/${id}/contract`);
    return data.payload;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function getWorker(id) {
  try {
    const { data } = await http.get(`/api/v1/workers/${id}`);
    return data.payload;
  } catch (error) {
    console.error(error);
    return null;
  }
}