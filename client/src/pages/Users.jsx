import { useState, useEffect, useContext, useCallback } from "react";
import { AuthContext } from "../context/AuthContext";
import { fetchUsers, disableUser, enableUser } from "../api/users";

const rolePriority = { admin: 1, moderator: 2, user: 3 }; // ✅ Define priority

const Users = () => {
  const { user } = useContext(AuthContext);
  const [activeUsers, setActiveUsers] = useState([]);
  const [disabledUsers, setDisabledUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processingUserId, setProcessingUserId] = useState(null);

  // ✅ Memoized function to fetch users only when needed
  const loadUsers = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchUsers();

      // ✅ Sort users by role (Admin > Moderator > User)
      const sortedUsers = data.sort((a, b) => rolePriority[a.role] - rolePriority[b.role]);

      setActiveUsers(sortedUsers.filter((u) => u.is_active));
      setDisabledUsers(sortedUsers.filter((u) => !u.is_active));
    } catch (err) {
      console.error("Error fetching users:", err);
      setError("Failed to load users.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]); // ✅ Fetch only when the function reference changes

  const handleDisable = async (userId) => {
    if (!window.confirm("Are you sure you want to disable this user?")) return;

    setProcessingUserId(userId);
    try {
      const token = localStorage.getItem("access_token");
      const success = await disableUser(userId, token);

      if (success) {
        setActiveUsers((prev) => prev.filter((u) => u.id !== userId));
        setDisabledUsers((prev) => [...prev, activeUsers.find((u) => u.id === userId)]);
      } else {
        alert("Failed to disable user.");
      }
    } catch (err) {
      console.error("Error disabling user:", err);
      alert("An error occurred while disabling the user.");
    } finally {
      setProcessingUserId(null);
    }
  };

  const handleEnable = async (userId) => {
    if (!window.confirm("Are you sure you want to enable this user?")) return;

    setProcessingUserId(userId);
    try {
      const token = localStorage.getItem("access_token");
      const success = await enableUser(userId, token);

      if (success) {
        setDisabledUsers((prev) => prev.filter((u) => u.id !== userId));
        setActiveUsers((prev) => [...prev, disabledUsers.find((u) => u.id === userId)]);
      } else {
        alert("Failed to enable user.");
      }
    } catch (err) {
      console.error("Error enabling user:", err);
      alert("An error occurred while enabling the user.");
    } finally {
      setProcessingUserId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p className="text-lg font-semibold animate-pulse text-gray-600">
          Loading users...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-64">
        <p className="text-red-500 text-lg font-semibold">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-lg rounded-lg">
      <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Users List</h1>

      {activeUsers.length === 0 ? (
        <p className="text-gray-600 text-center text-lg">No active users found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200 rounded-lg">
            <thead>
              <tr className="bg-gray-200 text-gray-700">
                <th className="py-3 px-6 text-left">Username</th>
                <th className="py-3 px-6 text-left">Role</th>
                <th className="py-3 px-6 text-left">Email</th>
                {user?.role === "admin" && <th className="py-3 px-6">Actions</th>}
              </tr>
            </thead>
            <tbody>
              {activeUsers.map((u) => (
                <tr key={u.id} className="border-b hover:bg-blue-50 transition">
                  <td className="py-3 px-6">{u.username}</td>
                  <td className="py-3 px-6">
                    <span className={`px-3 py-1 rounded-full text-sm ${u.role === "admin"
                      ? "bg-red-500 text-white"
                      : u.role === "moderator"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-400 text-white"}`}
                    >
                      {u.role.charAt(0).toUpperCase() + u.role.slice(1)}
                    </span>
                  </td>
                  <td className="py-3 px-6">{u.email}</td>
                  {user?.role === "admin" && (
                    <td className="py-3 px-6 text-center">
                      <button
                        onClick={() => handleDisable(u.id)}
                        disabled={processingUserId === u.id}
                        className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition disabled:bg-gray-400"
                      >
                        {processingUserId === u.id ? "Disabling..." : "Disable"}
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* 🔹 Show Disabled Users Section for Admins Only */}
      {user?.role === "admin" && disabledUsers.length > 0 && (
        <div className="mt-10">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">Disabled Users</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200 rounded-lg">
              <thead>
                <tr className="bg-gray-200 text-gray-700">
                  <th className="py-3 px-6 text-left">Username</th>
                  <th className="py-3 px-6 text-left">Role</th>
                  <th className="py-3 px-6 text-left">Email</th>
                  <th className="py-3 px-6">Actions</th>
                </tr>
              </thead>
              <tbody>
                {disabledUsers.map((u) => (
                  <tr key={u.id} className="border-b hover:bg-gray-100 transition">
                    <td className="py-3 px-6">{u.username}</td>
                    <td className="py-3 px-6">{u.role}</td>
                    <td className="py-3 px-6">{u.email}</td>
                    <td className="py-3 px-6 text-center">
                      <button
                        onClick={() => handleEnable(u.id)}
                        disabled={processingUserId === u.id}
                        className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition disabled:bg-gray-400"
                      >
                        {processingUserId === u.id ? "Enabling..." : "Enable"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Users;
