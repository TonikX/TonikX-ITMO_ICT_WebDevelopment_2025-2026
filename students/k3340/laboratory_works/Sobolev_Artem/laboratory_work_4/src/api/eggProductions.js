import http from "@/api/http.js";

export async function getEggProductions(chickenId) {
  try {
    const { data } = await http.get(`/api/v1/chickens/${chickenId}/egg-productions`);
    return data.payload || [];
  } catch (error) {
    console.error("Ошибка при получении производства яиц:", error);
    return [];
  }
}

export async function getEggProduction(chickenId, productionId) {
  try {
    const { data } = await http.get(`/api/v1/chickens/${chickenId}/egg-productions/${productionId}`);
    return data.payload || null;
  } catch (error) {
    console.error("Ошибка при получении записи производства:", error);
    return null;
  }
}

export async function createEggProduction(chickenId, production) {
  try {
    const { data } = await http.post(`/api/v1/chickens/${chickenId}/egg-productions`, production);
    return data;
  } catch (error) {
    console.error("Ошибка при создании записи производства:", error);
    return null;
  }
}