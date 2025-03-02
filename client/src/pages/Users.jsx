import { useState, useEffect } from "react";
import { fetchUsers } from "../api/users";

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const data = await fetchUsers();
        setUsers(data);
      } catch (err) {
        console.error("Error fetching users:", err); // ✅ Now 'err' is used
        setError("Failed to load users.");
      } finally {
        setLoading(false);
      }
    };

    loadUsers();
  }, []);

  if (loading) {
    return <p className="text-center text-lg font-semibold">Loading users...</p>;
  }

  if (error) {
    return <p className="text-red-500 text-center">{error}</p>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Users</h1>
      {users.length === 0 ? (
        <p>No users found.</p>
      ) : (
        <ul className="bg-gray-100 p-4 rounded shadow">
          {users.map((user) => (
            <li key={user.id} className="p-2 border-b">
              {user.username} - {user.email}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Users;

// The Users component fetches users from the API and displays them in a list. The useEffect hook is used to fetch the users when the component mounts. The users are stored in state using the useState hook. The component conditionally renders a message if no users are found, or a list of users if users are present.