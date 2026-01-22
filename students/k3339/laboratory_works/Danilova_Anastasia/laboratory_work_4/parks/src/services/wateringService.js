import axios from "axios";

const API_URL = "http://127.0.0.1:8000/parks";

export const getPlantWateringSchedule = async (plantId, token) => {
  console.log(`[wateringService] Getting schedule for plant ${plantId}`);

  try {
    const response = await axios.get(
      `${API_URL}/plants/${plantId}/plantwateringschedules/`,
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    console.log(
      `[wateringService] Success for plant ${plantId}:`,
      response.data
    );
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 404) {
      console.log(
        `[wateringService] No watering schedule found for plant ${plantId}`
      );
      return null;
    }

    console.error(`[wateringService] Error for plant ${plantId}:`, error);

    try {
      console.log(`[wateringService] Trying old endpoint for plant ${plantId}`);
      const oldResponse = await axios.get(
        `${API_URL}/plantwateringschedules/?plant=${plantId}`,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      const data = oldResponse.data;
      console.log(`[wateringService] Old endpoint response:`, data);

      if (data.results && data.results.length > 0) {
        return data.results[0];
      }
      if (Array.isArray(data) && data.length > 0) {
        return data[0];
      }
      return null;
    } catch (oldError) {
      console.error(
        `[wateringService] Both endpoints failed for plant ${plantId}:`,
        oldError
      );
      return null;
    }
  }
};

export const getPlantWateringSchedules = getPlantWateringSchedule;

export const createWateringSchedule = async (data, token) => {
  try {
    const response = await axios.post(
      `${API_URL}/plantwateringschedules/`,
      data,
      {
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error creating watering schedule:", error);
    throw error;
  }
};

export const updateWateringSchedule = async (id, data, token) => {
  try {
    const response = await axios.patch(
      `${API_URL}/plantwateringschedules/${id}/`,
      data,
      {
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error updating watering schedule:", error);
    throw error;
  }
};
