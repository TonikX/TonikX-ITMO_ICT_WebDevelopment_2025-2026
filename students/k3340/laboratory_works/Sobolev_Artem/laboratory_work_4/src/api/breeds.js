import http from "@/api/http.js";

export async function getBreeds() {
  const { data } = await http.get(`/api/v1/breeds/all`);
  return data.payload || [];
}

export async function getBreed(id) {
  try {
    const { data } = await http.get(`/api/v1/breeds/${id}`);
    return data.payload || [];
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function createBreed(breed) {
  const { data } = await http.post("/api/v1/breeds", breed);
  return data;
}