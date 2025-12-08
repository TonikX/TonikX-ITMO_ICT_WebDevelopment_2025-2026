import http from "@/api/http.js";

export async function getWorkshops() {
  const { data } = await http.get("/api/v1/workshops");
  return data.payload || [];
}


export async function getWorkshop(id) {
  try {
    const { data } = await http.get(`/api/v1/workshops/${id}`);
    return data.payload || [];
  } catch (error) {
    console.error("Ошибка при получении цеха:", error);
    return null;
  }
}

export async function createWorkshop(workshop) {
  try {
    const { data } = await http.post("/api/v1/workshops", workshop);
    return data;
  } catch (error) {
    console.error("Ошибка при создании цеха:", error);
    return null;
  }
}
