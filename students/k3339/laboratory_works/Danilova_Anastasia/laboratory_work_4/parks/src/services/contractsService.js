import axios from "axios";

const API_URL = "http://127.0.0.1:8000/parks";

export const getContracts = async (token, params = {}, page = 1) => {
  const queryParams = new URLSearchParams();

  Object.keys(params).forEach((key) => {
    if (params[key] !== undefined && params[key] !== null) {
      queryParams.append(key, params[key]);
    }
  });

  queryParams.append("page", page);

  const url = `${API_URL}/contracts/${
    queryParams.toString() ? `?${queryParams}` : ""
  }`;

  const response = await axios.get(url, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

export const getContractsByObject = async (objectId, token, page = 1) => {
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

export const getContractById = async (id, token) => {
  const response = await axios.get(`${API_URL}/contracts/${id}/`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

export const createContract = async (data, token) => {
  console.log("createContract called with data:", data);
  try {
    const response = await axios.post(`${API_URL}/contracts/`, data, {
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });
    console.log("createContract response:", response.data);
    return response.data;
  } catch (error) {
    console.error("createContract error:", error);
    console.error("Error response:", error.response?.data);
    throw error;
  }
};

export const updateContract = async (id, data, token) => {
  const response = await axios.patch(`${API_URL}/contracts/${id}/`, data, {
    headers: { Authorization: `Token ${token}` },
  });
  return response.data;
};

export const deleteContract = async (id, token) => {
  await axios.delete(`${API_URL}/contracts/${id}/`, {
    headers: { Authorization: `Token ${token}` },
  });
};
