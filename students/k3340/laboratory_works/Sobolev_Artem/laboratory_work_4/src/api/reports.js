import http from "@/api/http.js";

export async function getMonthlyFactoryReport(year, month) {
  try {
    const formattedMonth = month.toString().padStart(2, '0');

    const { data } = await http.get(`/api/v1/reports/director/factory/monthly`, {
      params: {
        year: year,
        month: formattedMonth
      }
    });
    return data.payload || null;
  } catch (error) {
    console.error("Ошибка при получении месячного отчета:", error);
    throw error;
  }
}

export async function getBreedEggDiffReport(year, month) {
  try {
    const formattedMonth = month.toString().padStart(2, '0');

    const { data } = await http.get(`/api/v1/reports/director/breeds/egg-diff`, {
      params: {
        year: year,
        month: formattedMonth
      }
    });
    return data.payload || [];
  } catch (error) {
    console.error("Ошибка при получении отчета по разнице яйценоскости:", error);
    throw error;
  }
}
