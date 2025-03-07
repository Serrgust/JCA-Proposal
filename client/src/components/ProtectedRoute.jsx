import PropTypes from "prop-types"; // ✅ Import PropTypes
import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <p>Loading...</p>;
  return user ? children : <Navigate to="/" />;
};

// ✅ Define prop types
ProtectedRoute.propTypes = {
  children: PropTypes.node.isRequired, // Ensure 'children' is validated
};

export default ProtectedRoute;
