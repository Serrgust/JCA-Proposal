export const fetchProposals = async (filters = {}) => {
  const params = new URLSearchParams(filters).toString(); // ✅ Convert filters to query params
  try {
    const response = await fetch(`http://localhost:5000/proposals?${params}`); // ✅ Append filters
    if (!response.ok) throw new Error("Failed to fetch proposals");
    return await response.json();
  } catch (error) {
    console.error("Error fetching proposals:", error);
    return [];
  }
};
