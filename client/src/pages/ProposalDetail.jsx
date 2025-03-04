import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { fetchProposalById } from "../api/proposals";
import { 
  BriefcaseIcon, MapPinIcon, CurrencyDollarIcon, DocumentTextIcon, 
  UserIcon, CalendarIcon, TagIcon, PencilSquareIcon, XCircleIcon 
} from "@heroicons/react/24/outline";

const ProposalDetail = () => {
  const { id } = useParams();
  const [proposal, setProposal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    const loadProposal = async () => {
      try {
        const data = await fetchProposalById(id);
        if (!data || Object.keys(data).length === 0) {
          throw new Error("Proposal not found");
        }
        setProposal(data);
        setFormData({
          resource_name: data.resource_name,
          opportunity_status: data.opportunity_status,
          business_unit: data.business_unit,
          client_name: data.client_name,
        });
      } catch (err) {
        console.error("Error fetching proposal:", err);
        setError("Failed to load proposal.");
      } finally {
        setLoading(false);
      }
    };

    loadProposal();
  }, [id]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`/proposals/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!response.ok) throw new Error("Failed to update proposal");

      const updatedProposal = await response.json();
      setProposal(updatedProposal);
      setIsEditing(false);
    } catch (error) {
      console.error("Error updating proposal:", error);
    }
  };

  if (loading) return <p className="text-center text-gray-600">Loading proposal details...</p>;
  if (error) return <p className="text-red-500 text-center">{error}</p>;
  if (!proposal) return <p className="text-gray-500 text-center">Proposal not found.</p>;

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg max-w-3xl mx-auto border">
      <h1 className="text-2xl font-bold mb-4 text-center flex items-center gap-2">
        <BriefcaseIcon className="w-6 h-6 text-gray-600" /> {proposal.name || "Unnamed Proposal"}
      </h1>

      {/* General Information - Now in a structured, unboxed format */}
      <div className="grid grid-cols-2 gap-4 text-sm">
        <p><strong>Client:</strong> {proposal.client || "N/A"}</p>
        <p><strong>Site:</strong> {proposal.site || "N/A"}</p>
        <p><strong>Quote Number:</strong> {proposal.quote_number || "N/A"}</p>
        <p><strong>Budget:</strong> {proposal.budget ? `$${proposal.budget}` : "Not specified"}</p>
        <p><strong>Resource Name:</strong> {proposal.resource_name || "N/A"}</p>
        <p><strong>Business Unit:</strong> {proposal.business_unit || "N/A"}</p>
        <p><strong>Opportunity Status:</strong> {proposal.opportunity_status || "N/A"}</p>
        <p><strong>Created:</strong> {new Date(proposal.created_at).toLocaleString()}</p>
        <p><strong>Updated:</strong> {new Date(proposal.updated_at).toLocaleString()}</p>
        <p><strong>Client Name:</strong> {proposal.client_name || "N/A"}</p>
      </div>

      {/* Description - Stays in a bordered box */}
      <div className="mt-4 p-4 bg-gray-50 border rounded-lg">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <DocumentTextIcon className="w-5 h-5 text-gray-500" /> Description:
        </h2>
        <p className="text-gray-700 mt-1">{proposal.description || "No description provided."}</p>
      </div>

      {/* Edit Button */}
      <div className="mt-6 text-center">
        <button
          onClick={() => setIsEditing(true)}
          className="bg-blue-500 text-white px-4 py-2 rounded flex items-center gap-1 hover:bg-blue-600 transition"
        >
          <PencilSquareIcon className="w-5 h-5" /> Edit Proposal
        </button>
      </div>

      {/* Custom Tailwind Modal */}
      {isEditing && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-bold">Edit Proposal</h2>
              <button onClick={() => setIsEditing(false)} className="text-gray-600 hover:text-gray-900">
                <XCircleIcon className="w-6 h-6" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="mt-4 space-y-3">
              <input type="text" name="resource_name" value={formData.resource_name} onChange={handleChange} className="border p-2 rounded w-full" placeholder="Resource Name" />
              <input type="text" name="opportunity_status" value={formData.opportunity_status} onChange={handleChange} className="border p-2 rounded w-full" placeholder="Opportunity Status" />
              <input type="text" name="business_unit" value={formData.business_unit} onChange={handleChange} className="border p-2 rounded w-full" placeholder="Business Unit" />
              <input type="text" name="client_name" value={formData.client_name} onChange={handleChange} className="border p-2 rounded w-full" placeholder="Client Name" />

              <div className="flex justify-end gap-3 mt-4">
                <button type="button" onClick={() => setIsEditing(false)} className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">Cancel</button>
                <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProposalDetail;
