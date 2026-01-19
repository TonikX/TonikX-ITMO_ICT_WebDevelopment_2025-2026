import axios from "axios";

const API_URL = "http://127.0.0.1:8000/parks";

export const updatePlant = async (id, data, token) => {
  console.log(`Updating plant ${id} with data:`, data);
  try {
    const response = await axios.patch(`${API_URL}/plants/${id}/`, data, {
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });
    console.log("Update response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Update plant error:", error.response?.data || error.message);
    throw error;
  }
};

export const getPlantsByObject = async (objectId, token, page = 1) => {
  try {
    const response = await axios.get(
      `${API_URL}/plantplacements/?object_id=${objectId}&page=${page}`,
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error loading plants by object:", error);
    throw error;
  }
};
export const getSpecies = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/species/`, {
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

export const createPlant = async (data, token) => {
  try {
    const response = await axios.post(`${API_URL}/plants/`, data, {
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating plant:", error);
    throw error;
  }
};

export const createPlantPlacement = async (data, token) => {
  try {
    const response = await axios.post(`${API_URL}/plantplacements/`, data, {
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating plant placement:", error);
    throw error;
  }
};
