import { http } from "./http";

export async function getWorkshops({ countChickens = false } = {}) {
  const res = await http.get("/workshops", {
    params: { count_chickens: countChickens },
  });
  return res.data;
}

export async function getWorkshopWithCages(
  workshopId,
  { countChickens = false } = {}
) {
  const res = await http.get(`/workshops/${workshopId}/cages`, {
    params: { count_chickens: countChickens },
  });
  return res.data;
}
