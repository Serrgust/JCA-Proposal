import { API_BASE_URL } from "../config";  // ✅ Import the global API URL


export const fetchProposals = async (filters = {}) => {
  const params = new URLSearchParams(filters).toString(); // Convert filters into query params
  try {
    const response = await fetch(`${API_BASE_URL}/proposals?${params}`); // Append filters to URL
    if (!response.ok) throw new Error("Failed to fetch proposals");
    return await response.json();
  } catch (error) {
    console.error("Error fetching proposals:", error);
    return [];
  }
};

export const fetchProposalById = async (id) => {
  const response = await fetch(`${API_BASE_URL}/proposals/${id}`);

  if (!response.ok) {
    throw new Error("Failed to fetch proposal");
  }

  return response.json();
};