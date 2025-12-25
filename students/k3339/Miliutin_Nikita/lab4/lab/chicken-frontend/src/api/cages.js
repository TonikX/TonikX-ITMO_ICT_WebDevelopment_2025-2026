import { http } from "./http";

export async function getCageWithChickens(cageId) {
  const res = await http.get(`/cages/${cageId}/chickens`);
  return res.data; // cage + chickens
}
