import axios from "axios";

const API_URL = "http://127.0.0.1:8000/parks";

export const getSpecies = async (token, page = 1) => {
  try {
    const response = await axios.get(`${API_URL}/species/?page=${page}`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error loading species:", error);
    throw error;
  }
};

export const getSpeciesById = async (id, token) => {
  const response = await axios.get(`${API_URL}/species/${id}/`, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};
