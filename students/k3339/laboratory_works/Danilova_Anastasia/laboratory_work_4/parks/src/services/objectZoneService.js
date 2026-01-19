import axios from "axios";

const API_URL = "http://127.0.0.1:8000/parks";

export const getZonesByObject = async (objectId, token) => {
  const response = await axios.get(
    `${API_URL}/objectzones/?object=${objectId}`,
    {
      headers: { Authorization: `Token ${token}` },
    }
  );
  return response.data;
};

export const createZone = async (data, token) => {
  const response = await axios.post(`${API_URL}/objectzones/`, data, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export const updateZone = async (id, data, token) => {
  const response = await axios.patch(`${API_URL}/objectzones/${id}/`, data, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export const deleteZone = async (id, token) => {
  await axios.delete(`${API_URL}/objectzones/${id}/`, {
    headers: { Authorization: `Token ${token}` },
  });
};
