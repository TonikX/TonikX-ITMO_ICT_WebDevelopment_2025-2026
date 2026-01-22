import axios from "axios";

const API_URL = "http://127.0.0.1:8000/parks";

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
