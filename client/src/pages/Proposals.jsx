import { useState, useEffect } from "react";
import { fetchProposals } from "../api/proposals";

const Proposals = () => {
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadProposals = async () => {
      try {
        const data = await fetchProposals();
        setProposals(data);
      } catch (err) {
        console.error("Error fetching proposals:", err);
        setError("Failed to load proposals.");
      } finally {
        setLoading(false);
      }
    };

    loadProposals();
  }, []);

  if (loading) {
    return <p className="text-center text-lg font-semibold">Loading proposals...</p>;
  }

  if (error) {
    return <p className="text-red-500 text-center">{error}</p>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Proposals</h1>
      {proposals.length === 0 ? (
        <p>No proposals found.</p>
      ) : (
        <ul className="bg-gray-100 p-4 rounded shadow">
          {proposals.map((proposal) => (
            <li key={proposal.id} className="p-2 border-b">
              <strong>{proposal.name}</strong> - {proposal.client} ({proposal.status})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Proposals;
