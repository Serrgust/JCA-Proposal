import { useState, useEffect, useCallback } from "react";
import { fetchProposals } from "../api/proposals";
import debounce from "lodash.debounce";  // ✅ Debounce for efficient API calls

const Proposals = () => {
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Filters
  const [client, setClient] = useState("");
  const [status, setStatus] = useState("");
  const [name, setName] = useState("");

  useEffect(() => {
    loadProposals();
  }, []);

  const loadProposals = async (filters = {}) => {
    setLoading(true);
    try {
      const data = await fetchProposals(filters);
      setProposals(data);
    } catch (err) {
      console.error("Error fetching proposals:", err);
      setError("Failed to load proposals.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadProposals({ name, client, status });
  };

  const clearFilters = () => {
    setName("");
    setClient("");
    setStatus("");
    loadProposals({}); // Fetch all proposals again
  };

  // ✅ Debounce API calls to prevent excessive requests
  const debouncedSearch = useCallback(
    debounce(() => {
      loadProposals({ name, client, status });
    }, 500), // Waits 1 second before making the API call
    [name, client, status]
  );

  useEffect(() => {
    debouncedSearch();
    return () => debouncedSearch.cancel(); // ✅ Cleanup debounce
  }, [debouncedSearch]);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Proposals</h1>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="flex flex-wrap gap-2 mb-4">
        <input
          type="text"
          placeholder="Search by Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border p-2 rounded w-1/3"
        />
        <input
          type="text"
          placeholder="Search by Client"
          value={client}
          onChange={(e) => setClient(e.target.value)}
          className="border p-2 rounded w-1/3"
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="border p-2 rounded w-1/4"
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="in_review">In Review</option>
        </select>
        <button
          type="button"
          onClick={clearFilters}
          className="bg-gray-500 text-white p-2 rounded"
        >
          Clear Filters
        </button>
      </form>

      {loading ? (
        <p className="text-center text-lg font-semibold">Loading proposals...</p>
      ) : error ? (
        <p className="text-red-500 text-center">{error}</p>
      ) : proposals.length === 0 ? (
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
