import { http } from "./http";

// список связей порода+сезон -> diet_id
export async function getBreedDietSeasons(params = {}) {
  const res = await http.get("/breed-diet-seasons", { params });
  return res.data;
}

// назначить/обновить диету для породы в сезон (upsert)
export async function upsertBreedDietForSeason(breedId, season, dietId) {
  const res = await http.put(`/breeds/${breedId}/diets/${season}`, { diet_id: dietId });
  return res.data;
}

// удалить связь
export async function deleteBreedDietSeason(breedId, season) {
  const res = await http.delete(`/breed-diet-seasons/${breedId}/${season}`);
  return res.data;
}
