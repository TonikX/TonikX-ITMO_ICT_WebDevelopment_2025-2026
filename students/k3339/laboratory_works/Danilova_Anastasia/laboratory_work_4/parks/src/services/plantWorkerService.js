import axios from "axios";

const API_URL = "http://127.0.0.1:8000/parks";

export const getPlantWorkerAssignments = async (plantId, token, page = 1) => {
  console.log(`[plantWorkerService] Getting assignments for plant ${plantId}`);

  try {
    const response = await axios.get(
      `${API_URL}/workerassignments/?plant=${plantId}`,
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    const data = response.data;
    console.log(`[plantWorkerService] Assignments for plant ${plantId}:`, data);

    return data;
  } catch (error) {
    console.error(
      `[plantWorkerService] Error loading assignments for plant ${plantId}:`,
      error
    );
    throw error;
  }
};

export const createPlantWorkerAssignment = async (data, token) => {
  console.log("[plantWorkerService] Creating plant worker assignment:", data);

  try {
    const response = await axios.post(`${API_URL}/workerassignments/`, data, {
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });

    console.log("[plantWorkerService] Create successful:", response.data);
    return response.data;
  } catch (error) {
    console.error("[plantWorkerService] Error creating:", error);

    if (error.response && error.response.status === 400) {
      console.error(
        "[plantWorkerService] Validation errors:",
        error.response.data
      );
      console.error(
        "[plantWorkerService] Full error response:",
        JSON.stringify(error.response.data, null, 2)
      );
    }

    throw error;
  }
};

export const updatePlantWorkerAssignment = async (id, data, token) => {
  console.log("[plantWorkerService] Updating plant worker assignment:", {
    id,
    data,
  });

  try {
    const response = await axios.patch(
      `${API_URL}/workerassignments/${id}/`,
      data,
      {
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    console.log("[plantWorkerService] Update successful:", response.data);
    return response.data;
  } catch (error) {
    console.error("[plantWorkerService] Error updating:", error);

    if (error.response && error.response.status === 400) {
      console.error(
        "[plantWorkerService] Validation errors:",
        error.response.data
      );
    }

    throw error;
  }
};

export const deletePlantWorkerAssignment = async (id, token) => {
  await axios.delete(`${API_URL}/workerassignments/${id}/`, {
    headers: { Authorization: `Token ${token}` },
  });
};

export const getObjectWorkers = async (objectId, token, page = 1) => {
  console.log(`[plantWorkerService] Getting workers for object ${objectId}`);

  try {
    const response = await axios.get(
      `${API_URL}/objectworkers/?object=${objectId}&page=${page}`,
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    const data = response.data;
    console.log(`[plantWorkerService] Object workers response:`, data);

    return data.results || data || [];
  } catch (error) {
    console.error(`[plantWorkerService] Error loading object workers:`, error);
    console.error(`[plantWorkerService] Error details:`, error.response?.data);
    throw error;
  }
};

export const getAllWorkers = async (token) => {
  let allWorkers = [];
  let nextUrl = `${API_URL}/workers/`;

  while (nextUrl) {
    const response = await axios.get(nextUrl, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    const data = response.data;
    allWorkers = [...allWorkers, ...(data.results || [])];
    nextUrl = data.next;
  }

  return allWorkers;
};
export const getObjectWorkerAssignments = async (objectId, token, page = 1) => {
  const response = await axios.get(
    `${API_URL}/objectworkers/?object=${objectId}&page=${page}`,
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );
  return response.data;
};

export const createObjectWorkerAssignment = async (data, token) => {
  console.log("[plantWorkerService] Creating object worker assignment:", data);
  console.log("[plantWorkerService] URL:", `${API_URL}/objectworkers/`);

  try {
    const response = await axios.post(`${API_URL}/objectworkers/`, data, {
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });

    console.log("[plantWorkerService] Create successful:", response.data);
    return response.data;
  } catch (error) {
    console.error("[plantWorkerService] Error creating:", error);

    if (error.response) {
      console.error("[plantWorkerService] Status:", error.response.status);
      console.error("[plantWorkerService] Headers:", error.response.headers);
      console.error("[plantWorkerService] Data:", error.response.data);
      console.error(
        "[plantWorkerService] Full error:",
        JSON.stringify(error.response.data, null, 2)
      );
    } else if (error.request) {
      console.error(
        "[plantWorkerService] No response received:",
        error.request
      );
    } else {
      console.error(
        "[plantWorkerService] Error setting up request:",
        error.message
      );
    }

    throw error;
  }
};

export const updateObjectWorkerAssignment = async (id, data, token) => {
  console.log("[plantWorkerService] Updating object worker assignment:", {
    id,
    data,
  });

  try {
    const response = await axios.patch(
      `${API_URL}/objectworkers/${id}/`,
      data,
      {
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    console.log("[plantWorkerService] Update successful:", response.data);
    return response.data;
  } catch (error) {
    console.error("[plantWorkerService] Error updating:", error);
    console.error("[plantWorkerService] Error response:", error.response?.data);
    throw error;
  }
};

export const deleteObjectWorkerAssignment = async (id, token) => {
  try {
    await axios.delete(`${API_URL}/objectworkers/${id}/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
  } catch (error) {
    console.error("Error deleting object worker assignment:", error);
    throw error;
  }
};
