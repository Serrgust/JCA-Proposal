import { useState, useEffect, useCallback } from "react";
import { fetchProposals } from "../api/proposals";
import { Link } from "react-router-dom";
import debounce from "lodash.debounce";
import { Transition } from "@headlessui/react";
import { MagnifyingGlassIcon, XCircleIcon, ArrowPathIcon } from "@heroicons/react/24/outline";

const Proposals = () => {
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Filters
  const [client, setClient] = useState("");
  const [clientName, setClientName] = useState("");
  const [name, setName] = useState("");

  // Sorting
  const [sortBy, setSortBy] = useState("newest");

  useEffect(() => {
    loadProposals();
  }, []);

  const loadProposals = async (filters = {}) => {
    setLoading(true);
    try {
      const data = await fetchProposals({ ...filters });

      if (!data || !Array.isArray(data)) {
        throw new Error("Invalid API response");
      }

      // Apply sorting before setting state
      const sortedData = sortProposals(data, sortBy);
      setProposals(sortedData);
    } catch (err) {
      console.error("Error fetching proposals:", err);
      setError("Failed to load proposals.");
      setProposals([]);
    } finally {
      setLoading(false);
    }
  };

  // Sort Proposals based on user selection
  const sortProposals = (data, sortType) => {
    return [...data].sort((a, b) => {
      if (sortType === "newest") {
        return new Date(b.created_at) - new Date(a.created_at);
      }
      if (sortType === "alphabetical") {
        return a.name.localeCompare(b.name);
      }
      return 0;
    });
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadProposals({ name, client, client_name: clientName });
  };

  const clearFilters = () => {
    setName("");
    setClient("");
    setClientName("");
    loadProposals({});
  };

  // ✅ Debounce API calls to prevent excessive requests
  const debouncedSearch = useCallback(
    debounce(() => {
      loadProposals({ name, client, client_name: clientName });
    }, 500),
    [name, client, clientName, sortBy]
  );

  useEffect(() => {
    debouncedSearch();
    return () => debouncedSearch.cancel();
  }, [debouncedSearch]);

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-center flex items-center gap-2">
        <MagnifyingGlassIcon className="w-6 h-6 text-gray-600" /> Proposals
      </h1>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-4">
        {/* First Row: Search Fields */}
        <div className="grid grid-cols-3 gap-3">
          {/* Name Search */}
          <div className="relative flex items-center">
            <MagnifyingGlassIcon className="absolute left-2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Search by Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="border p-2 pl-8 rounded w-full"
            />
          </div>
          {/* Client Search */}
          <div className="relative flex items-center">
            <MagnifyingGlassIcon className="absolute left-2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Search by Client"
              value={client}
              onChange={(e) => setClient(e.target.value)}
              className="border p-2 pl-8 rounded w-full"
            />
          </div>
          {/* Client Name Search */}
          <div className="relative flex items-center">
            <MagnifyingGlassIcon className="absolute left-2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Search by Client Name"
              value={clientName}
              onChange={(e) => setClientName(e.target.value)}
              className="border p-2 pl-8 rounded w-full"
            />
          </div>
        </div>

        {/* Second Row: Clear Filters & Sorting Dropdown */}
        <div className="flex justify-between mt-3">
          {/* Clear Filters Button */}
          <button
            type="button"
            onClick={clearFilters}
            className="bg-gray-500 text-white px-4 py-2 rounded flex items-center gap-1 hover:bg-gray-600 transition"
          >
            <XCircleIcon className="w-5 h-5" /> Clear Filters
          </button>

          {/* Sorting Dropdown */}
          <select
            value={sortBy}
            onChange={(e) => {
              setSortBy(e.target.value);
              setProposals(sortProposals(proposals, e.target.value));
            }}
            className="border p-2 rounded bg-white shadow-sm"
          >
            <option value="newest">Sort by Newest</option>
            <option value="alphabetical">Sort Alphabetically</option>
          </select>
        </div>
      </form>

      {/* Loading Animation */}
      <Transition
        show={loading}
        enter="transition-opacity duration-300"
        enterFrom="opacity-0"
        enterTo="opacity-100"
        leave="transition-opacity duration-300"
        leaveFrom="opacity-100"
        leaveTo="opacity-0"
      >
        <p className="text-center text-lg font-semibold flex items-center justify-center gap-2">
          <ArrowPathIcon className="w-6 h-6 animate-spin text-gray-600" />
          Loading proposals...
        </p>
      </Transition>

      {/* Error Handling */}
      {error && <p className="text-red-500 text-center">{error}</p>}

      {/* Proposal List */}
      {!loading && proposals.length === 0 ? (
        <p className="text-center text-gray-500">No proposals found.</p>
      ) : (
        <ul className="bg-gray-100 p-4 rounded shadow mt-4 divide-y">
          {proposals.map((proposal) => (
            <li key={proposal.id} className="p-3 hover:bg-gray-200 transition">
              <Link to={`/proposals/${proposal.id}`} className="text-blue-500 flex justify-between">
                <span className="font-semibold">{proposal.name}</span>
                <span className="text-gray-600">{proposal.client || proposal.client_name}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Proposals;
