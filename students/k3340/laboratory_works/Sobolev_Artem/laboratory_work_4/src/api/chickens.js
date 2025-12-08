import http from "@/api/http.js";

export async function getChickens() {
  const { data } = await http.get("/api/v1/chickens");
  return data.payload || [];
}

export async function getChicken(id) {
  try {
    const response = await http.get(`/api/v1/chickens/${id}`);
    return {
      data: response.data.payload || null,
    };
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function createChicken(chicken) {
  const { data } = await http.post("/api/v1/chickens", chicken);
  return data;
}
