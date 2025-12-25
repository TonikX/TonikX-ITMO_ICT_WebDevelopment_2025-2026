import { http } from "./http";

export async function getChicken(chickenId) {
  const res = await http.get(`/chickens/${chickenId}`);
  return res.data;
}

export async function moveChicken(chickenId, { to_cage_id, moved_at }) {
  const res = await http.post(`/chickens/${chickenId}/move`, {
    chicken_id: Number(chickenId),
    to_cage_id: Number(to_cage_id),
    moved_at: moved_at ?? new Date().toISOString(),
  });
  return res.data;
}
