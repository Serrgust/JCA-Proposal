import { Link } from "react-router-dom";
import { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import LoginModal from "./LoginModal";
import RegisterModal from "./RegisterModal"; // ✅ Import Register Modal

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const [isLoginOpen, setLoginOpen] = useState(false);
  const [isRegisterOpen, setRegisterOpen] = useState(false); // ✅ Track Register Modal

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        {/* ✅ Show Logged-In User Info */}
        <div className="flex items-center space-x-3">
          <Link to="/" className="text-lg font-bold">MyApp</Link>
          {user && (
            <span className="text-sm bg-gray-700 px-3 py-1 rounded">
              Welcome, {user.username} ({user.role})
            </span>
          )}
        </div>

        <div className="flex items-center space-x-4">
          {user ? (
            <>
              <Link to="/users" className="hover:text-gray-300">Users</Link>
              <Link to="/proposals" className="hover:text-gray-300">Proposals</Link>
              <Link to="/add-proposal" className="bg-blue-500 px-4 py-2 rounded hover:bg-blue-600">
                Add Proposal
              </Link>

              {/* ✅ Register Button Now Between "Add Proposal" and "Logout" */}
              <button 
                onClick={() => setRegisterOpen(true)} 
                className="bg-yellow-500 px-4 py-2 rounded hover:bg-yellow-600"
              >
                Register
              </button>

              <button onClick={logout} className="bg-red-500 px-4 py-2 rounded hover:bg-red-600">
                Logout
              </button>
            </>
          ) : (
            <>
              <button 
                onClick={() => setLoginOpen(true)} 
                className="bg-green-500 px-4 py-2 rounded hover:bg-green-600"
              >
                Login
              </button>
              <button 
                onClick={() => setRegisterOpen(true)} 
                className="bg-yellow-500 px-4 py-2 rounded hover:bg-yellow-600"
              >
                Register
              </button>
            </>
          )}
        </div>
      </div>

      {/* Render Modals */}
      <LoginModal isOpen={isLoginOpen} onClose={() => setLoginOpen(false)} />
      <RegisterModal 
        isOpen={isRegisterOpen} 
        onClose={() => setRegisterOpen(false)} 
        isAdmin={user?.role === "admin"} // ✅ Pass admin check to RegisterModal
      />
    </nav>
  );
};

export default Navbar;
