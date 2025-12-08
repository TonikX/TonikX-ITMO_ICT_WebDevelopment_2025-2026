import http from "@/api/http.js";

export async function getRows(workshopId) {
  try {
    const { data } = await http.get(`/api/v1/workshops/${workshopId}/rows`);
    return data.payload || [];
  } catch (error) {
    console.error("Ошибка при получении клеток:", error);
    return [];
  }
}

export async function createRow(workshopId, row) {
  try {
    console.log("API запрос: создание ряда", {
      workshopId,
      row,
      url: `/api/v1/workshops/${workshopId}/rows`
    });

    const { data } = await http.post(`/api/v1/workshops/${workshopId}/rows`, row);

    console.log("API ответ:", data);

    if (data.success === false) {
      throw new Error(data.message || "Не удалось создать ряд");
    }

    return data.payload || data;
  } catch (error) {
    console.error("Детальная ошибка API при создании ряда:", {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      workshopId,
      row
    });

    throw error;
  }
}