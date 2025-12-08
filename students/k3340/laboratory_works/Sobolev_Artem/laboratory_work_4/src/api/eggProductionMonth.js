import http from "@/api/http.js";

export async function getLastEggProduction(chickenId) {
  try {
    const { data } = await http.get(`/api/v1/chickens/${chickenId}/egg-productions`);
    const productions = data.payload || [];

    if (!productions.length) return 0;

    productions.sort((a, b) => {
      if (a.year === b.year) return b.month - a.month;
      return b.year - a.year;
    });

    return productions[0].count || 0;
  } catch (error) {
    console.error("Ошибка при получении последних данных о яйцах:", error);
    return 0;
  }
}