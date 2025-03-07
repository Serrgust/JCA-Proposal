import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { fetchProposalById, updateProposal } from "../api/proposals";
import {
  BriefcaseIcon, MapPinIcon, CurrencyDollarIcon, DocumentTextIcon, UserIcon,
  CalendarIcon, PencilSquareIcon, IdentificationIcon, BuildingOfficeIcon,
  ClipboardDocumentCheckIcon, ClipboardIcon, ClockIcon
} from "@heroicons/react/24/outline";

const ProposalDetail = ({ proposalId }) => {
  const [proposal, setProposal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});

  useEffect(() => {
    const loadProposal = async () => {
      if (!proposalId) return;
      setLoading(true);
      try {
        const data = await fetchProposalById(proposalId);
        if (!data || Object.keys(data).length === 0) {
          throw new Error("Proposal not found");
        }
        setProposal(data);
        setFormData({
          name: data.name || "",
          client: data.client || "",
          site: data.site || "",
          quote_number: data.quote_number || "",
          client_name: data.client_name || "",
          budget: data.budget || "",
          description: data.description || "",
          resource_name: data.resource_name || "",
          business_unit: data.business_unit || "",
          opportunity_status: data.opportunity_status || "",
        });
      } catch (err) {
        console.error("Error fetching proposal:", err);
        setProposal(null);
      } finally {
        setLoading(false);
      }
    };

    loadProposal();
  }, [proposalId]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors((prev) => ({ ...prev, [e.target.name]: "" }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    console.log("Submitting form..."); // ✅ Debugging log
  
    let newErrors = {};
    if (!formData.name.trim()) newErrors.name = "Proposal Name is required.";
    if (!formData.client.trim()) newErrors.client = "Client is required.";
    if (!formData.client_name.trim()) newErrors.client_name = "Client Name is required.";
    if (!formData.quote_number.trim()) newErrors.quote_number = "Quote Number is required.";
    if (!formData.site.trim()) newErrors.site = "Site is required.";
    if (!formData.opportunity_status.trim()) newErrors.opportunity_status = "Opportunity Status is required.";
  
    if (Object.keys(newErrors).length > 0) {
      console.log("Validation failed:", newErrors); // ✅ Debugging
      setErrors(newErrors);
      return;
    }
  
    try {
      const response = await updateProposal(proposalId, formData);
      console.log("Proposal updated:", response); // ✅ Debugging
  
      setProposal((prev) => ({ ...prev, ...formData })); // ✅ Update state
      setIsEditing(false); // ✅ Exit edit mode
    } catch (err) {
      console.error("Error updating proposal:", err);
    }
  };

  if (loading) return <p className="text-gray-600 text-center">Loading proposal details...</p>;
  if (!proposal) return <p className="text-red-500 text-center">Proposal not found.</p>;

  return (
    <div className="p-6 rounded-lg max-w-4xl mx-auto">
      <h2 className="text-lg font-bold flex items-center gap-2">
        <BriefcaseIcon className="w-5 h-5 text-gray-600" /> {proposal.name || "Unnamed Proposal"}
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-2 gap-4 text-lg mt-3 text-gray-700">
          {[
            { label: "Client", name: "client", icon: <UserIcon className="w-5 h-5" /> },
            { label: "Client Name", name: "client_name", icon: <UserIcon className="w-5 h-5" /> },
            { label: "Site", name: "site", icon: <MapPinIcon className="w-5 h-5" /> },
            { label: "Quote Number", name: "quote_number", icon: <ClipboardIcon className="w-5 h-5" /> },
            { label: "Budget ($)", name: "budget", type: "number", icon: <CurrencyDollarIcon className="w-5 h-5" /> },
            { label: "Business Unit", name: "business_unit", icon: <BuildingOfficeIcon className="w-5 h-5" /> },
            { label: "Opportunity Status", name: "opportunity_status", icon: <ClipboardDocumentCheckIcon className="w-5 h-5" />, type: "dropdown" },
            { label: "Resource Name", name: "resource_name", icon: <IdentificationIcon className="w-5 h-5" /> },
          ].map((field) => (
            <div key={field.name}>
              <label className="text-sm font-large flex items-center gap-2">
                {field.icon} {field.label}
              </label>
              {isEditing ? (
                field.type === "dropdown" ? (
                  <select
                    name={field.name}
                    value={formData[field.name]}
                    onChange={handleChange}
                    className="w-max text-lg border p-2 rounded"
                  >
                    <option value="Quote">Quote</option>
                    <option value="Approved">Approved</option>
                    <option value="Rejected">Rejected</option>
                    <option value="Pending">Pending</option>
                  </select>
                ) : (
                  <input
                    type={field.type || "text"}
                    name={field.name}
                    value={formData[field.name]}
                    onChange={handleChange}
                    className="w-max text-lg border p-2 rounded"
                  />
                )
              ) : (
                <p className="text-black">{proposal[field.name] || "N/A"}</p>
              )}
            </div>
          ))}
        </div>

        {/* Updated Date (ABOVE Description) */}
        <p className="mt-4 text-sm flex items-center gap-2 text-gray-800">
          <ClockIcon className="w-5 h-5 text-gray-500" /> <strong>Updated:</strong> {new Date(proposal.updated_at).toLocaleString()}
        </p>

        {/* Description */}
        <div className="mt-3 p-3 bg-gray-50 border rounded-lg">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <DocumentTextIcon className="w-5 h-5 text-gray-500" /> Description:
          </h2>
          {isEditing ? (
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="w-full border p-2 rounded"
            />
          ) : (
            <p className="text-gray-700 mt-1">{proposal.description || "No description provided."}</p>
          )}
        </div>

        {/* Created By and Dates */}
        <div className="mt-3 text-sm flex justify-between">
          <p className="flex items-center gap-2">
            <UserIcon className="w-5 h-5 text-gray-500" /> <strong>Created By:</strong> {proposal.created_by?.first_name} {proposal.created_by?.last_name}
          </p>
          <p className="flex items-center gap-2">
            <CalendarIcon className="w-5 h-5 text-gray-500" /> <strong>Created:</strong> {new Date(proposal.created_at).toLocaleString()}
          </p>
        </div>

        {/* Edit Buttons */}
        <div className="mt-3 text-center">
          {isEditing ? (
            <div className="flex justify-between">
              <button type="button" onClick={() => setIsEditing(false)} className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">
                Cancel
              </button>
              <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                Save Changes
              </button>
            </div>
          ) : (
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              className="bg-blue-500 text-white px-4 py-2 rounded flex items-center gap-1 hover:bg-blue-600 transition"
            >
              <PencilSquareIcon className="w-5 h-5" /> Edit Proposal
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

// ✅ Add PropTypes validation
ProposalDetail.propTypes = {
  proposalId: PropTypes.number.isRequired, // Ensures proposalId is a number and required
};

export default ProposalDetail;
