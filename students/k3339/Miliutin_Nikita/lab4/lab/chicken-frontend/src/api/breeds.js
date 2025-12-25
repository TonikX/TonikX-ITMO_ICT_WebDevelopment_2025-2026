import { http } from "./http";

export async function getBreeds(params = {}) {
  const res = await http.get("/breeds", { params });
  return res.data;
}
