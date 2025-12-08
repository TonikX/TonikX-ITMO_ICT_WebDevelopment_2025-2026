import http from "@/api/http.js";

export async function getDiets() {
  const { data } = await http.get("/api/v1/diets");
  return data.payload || [];
}

export async function getDiet(id) {
  try {
    const { data } = await http.get(`/api/v1/diets/${id}`);
    return data.payload || [];
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function createDiet(diet) {
  const { data } = await http.post("/api/v1/diets", diet);
  return data;
}