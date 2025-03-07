import { API_BASE_URL } from "../config"; // ✅ Import the global API URL

export const fetchUsers = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/all`);
    if (!response.ok) {
      const errorData = await response.json();
      console.error("API Error:", errorData);
      throw new Error("Failed to fetch users");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching users:", error);
    return [];
  }
};


export const disableUser = async (userId, token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/disable`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`, // ✅ Send JWT for authentication
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to disable user");
    }

    return true; // ✅ Return true on success
  } catch (error) {
    console.error("Error disabling user:", error);
    return false; // ✅ Return false if failure
  }
};

export const enableUser = async (userId, token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/enable`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to enable user");
    }

    return true;
  } catch (error) {
    console.error("Error enabling user:", error);
    return false;
  }
};