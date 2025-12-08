import http from "@/api/http.js";

export async function getCages(rowId) {
  try {
    const { data } = await http.get(`/api/v1/rows/${rowId}/cage`);
    return data.payload || [];
  } catch (error) {
    console.error("Ошибка при получении клеток:", error);
    return [];
  }
}

export async function getCage(rowId, cageNumber) {
  try {
    const { data } = await http.get(`/api/v1/rows/${rowId}/cage/${cageNumber}`);
    return data.payload || null;
  } catch (error) {
    console.error("Ошибка при получении клетки:", error);
    return null;
  }
}

export async function createCage(rowId, cage) {
  try {
    const { data } = await http.post(`/api/v1/rows/${rowId}/cage`, cage);
    return data;
  } catch (error) {
    console.error("Ошибка при создании клетки:", error);
    return null;
  }
}