import axios from "axios";

const API_URL = "http://127.0.0.1:8000/parks";

export const getObjects = async (token, page = 1) => {
  const response = await axios.get(`${API_URL}/objects/?page=${page}`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

export const getObjectById = async (id, token) => {
  const response = await axios.get(`${API_URL}/objects/${id}/`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

export const createObject = async (data, token) => {
  const response = await axios.post(`${API_URL}/objects/`, data, {
    headers: {
      Authorization: `Token ${token}`,
      "Content-Type": "application/json",
    },
  });
  return response.data;
};

export const updateObject = async (id, data, token) => {
  const response = await axios.patch(`${API_URL}/objects/${id}/`, data, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export const deleteObject = async (id, token) => {
  await axios.delete(`${API_URL}/objects/${id}/`, {
    headers: { Authorization: `Token ${token}` },
  });
};

export const getDecorators = async (token) => {
  const response = await axios.get(`${API_URL}/decorators/`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  console.log("Decorators response:", response.data);
  return response.data;
};

export const getObjectZones = async (objectId, token) => {
  const response = await axios.get(
    `${API_URL}/objectzones/?object=${objectId}`,
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );
  return response.data;
};

export const createObjectZone = async (data, token) => {
  const response = await axios.post(`${API_URL}/objectzones/`, data, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export const updateObjectZone = async (id, data, token) => {
  const response = await axios.patch(`${API_URL}/objectzones/${id}/`, data, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export const deleteObjectZone = async (id, token) => {
  await axios.delete(`${API_URL}/objectzones/${id}/`, {
    headers: { Authorization: `Token ${token}` },
  });
};

export const getObjectContracts = async (objectId, token, page = 1) => {
  const response = await axios.get(
    `${API_URL}/contracts/?object=${objectId}&page=${page}`,
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );
  return response.data;
};
