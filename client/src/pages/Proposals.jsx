import { useState, useEffect, useCallback, useMemo } from "react";
import { fetchProposals } from "../api/proposals";
import ProposalDetail from "./ProposalDetail";
import { MagnifyingGlassIcon, XCircleIcon, ArrowPathIcon, ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/24/outline";
import { Transition } from "@headlessui/react";
import debounce from "lodash.debounce";

const Proposals = () => {
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expandedProposal, setExpandedProposal] = useState(null);

  // Filters
  const [filters, setFilters] = useState({ name: "", client: "", clientName: "" });

  // Sorting
  const [sortBy, setSortBy] = useState("newest");

  // ✅ Memoized API call to prevent unnecessary re-fetching
  const loadProposals = useCallback(async (filters = {}) => {
    setLoading(true);
    try {
      const data = await fetchProposals({ ...filters });

      if (!data || !Array.isArray(data)) {
        throw new Error("Invalid API response");
      }

      setProposals(data); // ✅ Store proposals without modifying sort order yet
    } catch (err) {
      console.error("Error fetching proposals:", err);
      setError("Failed to load proposals.");
      setProposals([]);
    } finally {
      setLoading(false);
    }
  }, []);

  // ✅ Fetch proposals when the component mounts
  useEffect(() => {
    loadProposals();
  }, [loadProposals]); // ✅ Now `loadProposals` is initialized before useEffect runs

  // ✅ Debounced search function to prevent excessive API calls
  const debouncedSearch = useCallback(
    debounce(() => {
      loadProposals({ name: filters.name, client: filters.client, client_name: filters.clientName });
    }, 500),
    [filters, loadProposals] // ✅ Re-run when filters change
  );

  useEffect(() => {
    debouncedSearch();
    return () => debouncedSearch.cancel();
  }, [debouncedSearch]);

  // ✅ Memoized sorting logic to prevent unnecessary computations
  const sortedProposals = useMemo(() => {
    return [...proposals].sort((a, b) => {
      if (sortBy === "newest") return new Date(b.created_at) - new Date(a.created_at);
      if (sortBy === "alphabetical") return a.name.localeCompare(b.name);
      return 0;
    });
  }, [proposals, sortBy]);

  const toggleProposalDetails = (proposalId) => {
    setExpandedProposal((prevId) => (prevId === proposalId ? null : proposalId));
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-center flex items-center gap-2">
        <MagnifyingGlassIcon className="w-6 h-6 text-gray-600" /> Proposals
      </h1>

      <form className="mb-4">
        <div className="grid grid-cols-3 gap-3">
          {["name", "client", "clientName"].map((filterKey, index) => (
            <div key={index} className="relative flex items-center">
              <MagnifyingGlassIcon className="absolute left-2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                placeholder={`Search by ${filterKey.replace("Name", " Name")}`}
                value={filters[filterKey]}
                onChange={(e) => setFilters((prev) => ({ ...prev, [filterKey]: e.target.value }))}
                className="border p-2 pl-8 rounded w-full"
              />
            </div>
          ))}
        </div>

        <div className="flex justify-between mt-3">
          <button
            type="button"
            onClick={() => setFilters({ name: "", client: "", clientName: "" })}
            className="bg-gray-500 text-white px-4 py-2 rounded flex items-center gap-1 hover:bg-gray-600 transition"
          >
            <XCircleIcon className="w-5 h-5" /> Clear Filters
          </button>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="border p-2 rounded bg-white shadow-sm"
          >
            <option value="newest">Sort by Newest</option>
            <option value="alphabetical">Sort Alphabetically</option>
          </select>
        </div>
      </form>

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

      {error && <p className="text-red-500 text-center">{error}</p>}

      {!loading && sortedProposals.length === 0 ? (
        <p className="text-center text-gray-500">No proposals found.</p>
      ) : (
        <ul className="bg-gray-100 p-4 rounded shadow mt-4 divide-y">
          {sortedProposals.map((proposal) => (
            <li key={proposal.id} className="p-3">
              <button
                onClick={() => toggleProposalDetails(proposal.id)}
                className="w-full flex justify-between items-center text-left text-blue-500 font-semibold hover:underline"
              >
                <span>{proposal.name}</span>
                {expandedProposal === proposal.id ? (
                  <ChevronUpIcon className="w-5 h-5 text-gray-500" />
                ) : (
                  <ChevronDownIcon className="w-5 h-5 text-gray-500" />
                )}
              </button>

              <Transition
                show={expandedProposal === proposal.id}
                enter="transition-all duration-300 ease-in-out"
                enterFrom="max-h-0 opacity-0"
                enterTo="max-h-screen opacity-100"
                leave="transition-all duration-300 ease-in-out"
                leaveFrom="max-h-screen opacity-100"
                leaveTo="max-h-0 opacity-0"
              >
                <div className="mt-2 bg-white border rounded-lg p-4 shadow">
                  <ProposalDetail proposalId={proposal.id} />
                </div>
              </Transition>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Proposals;
