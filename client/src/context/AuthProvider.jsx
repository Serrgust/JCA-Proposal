import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import { AuthContext } from "./AuthContext"; // ✅ Import Context

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      axios
        .get("http://localhost:5000/auth/me", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          setUser(res.data);
        })
        .catch(() => {
          localStorage.removeItem("access_token");
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    try {
      const res = await axios.post("http://localhost:5000/auth/login", {
        email,
        password,
      });

      localStorage.setItem("access_token", res.data.access_token);
      setUser(await fetchUser());
      return true;
    } catch (error) {
      console.error("Login failed:", error.response?.data);
      return false;
    }
  };

  const fetchUser = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return null;

    try {
      const res = await axios.get("http://localhost:5000/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      return res.data;
    } catch {
      return null;
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// ✅ Define PropTypes to remove ESLint warnings
AuthProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export default AuthProvider;
