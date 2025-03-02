export const fetchProposals = async () => {
    try {
      const response = await fetch("http://localhost:5000/proposals"); // Replace with your backend URL
      if (!response.ok) throw new Error("Failed to fetch proposals");
      return await response.json();
    } catch (error) {
      console.error("Error fetching proposals:", error);
      return [];
    }
  };
  