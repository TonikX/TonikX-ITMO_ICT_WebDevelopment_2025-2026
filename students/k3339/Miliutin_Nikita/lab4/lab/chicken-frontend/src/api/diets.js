import { http } from "./http";

export async function getDiets(params = {}) {
  const res = await http.get("/diets/", { params });
  return res.data;
}

export async function getDiet(dietId) {
  const res = await http.get(`/diets/${dietId}`);
  return res.data;
}

export async function createDiet(payload) {
  const res = await http.post("/diets/", payload);
  return res.data;
}

export async function deleteDiet(dietId) {
  const res = await http.delete(`/diets/${dietId}`);
  return res.data; // 204 -> обычно undefined, но ок
}

// (не обязательно, но удобно на будущее)
export async function updateDiet(dietId, payload) {
  const res = await http.patch(`/diets/${dietId}`, payload);
  return res.data;
}
