import axios from "axios";

const API_URL = "http://127.0.0.1:8000/parks";

export const getEnterprises = async (token, page = 1) => {
  const response = await axios.get(`${API_URL}/enterprises/?page=${page}`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

export const getAllEnterprises = async (token) => {
  let allEnterprises = [];
  let nextUrl = `${API_URL}/enterprises/`;

  while (nextUrl) {
    const response = await axios.get(nextUrl, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    const data = response.data;
    allEnterprises = [...allEnterprises, ...(data.results || [])];
    nextUrl = data.next;
  }

  return allEnterprises;
};

export const getEnterpriseById = async (id, token) => {
  const response = await axios.get(`${API_URL}/enterprises/${id}/`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};
