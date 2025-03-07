import { useState, useContext } from "react";
import PropTypes from "prop-types";
import { Dialog, Transition } from "@headlessui/react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const LoginModal = ({ isOpen, onClose }) => {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const success = await login(email, password);
    if (success) {
      navigate("/"); // Redirect to home page after login
      onClose(); // Close modal after login
    } else {
      setError("Invalid email or password");
    }
  };

  return (
    <Transition show={isOpen} as="div" className="relative z-50">
      <Dialog as="div" className="fixed inset-0 overflow-y-auto" onClose={onClose}>
        <div className="flex items-center justify-center min-h-screen p-4">
          <Transition.Child
            as="div"
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
            className="fixed inset-0 bg-black bg-opacity-50"
          />
          <Transition.Child
            as="div"
            enter="ease-out duration-300 transform"
            enterFrom="opacity-0 scale-95"
            enterTo="opacity-100 scale-100"
            leave="ease-in duration-200 transform"
            leaveFrom="opacity-100 scale-100"
            leaveTo="opacity-0 scale-95"
            className="bg-white p-6 rounded-lg shadow-lg w-96 relative z-10"
          >
            <Dialog.Title className="text-2xl font-semibold text-center text-gray-900">Login</Dialog.Title>

            <form onSubmit={handleSubmit} className="space-y-4 mt-4">
              <div>
                <label className="block text-gray-700 font-medium">Email</label>
                <input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>

              <div>
                <label className="block text-gray-700 font-medium">Password</label>
                <input
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-blue-500 text-white p-3 rounded hover:bg-blue-600 transition"
              >
                Login
              </button>
            </form>

            {error && <p className="text-red-500 text-sm mt-2 text-center">{error}</p>}

            {/* Close Button */}
            <button
              onClick={onClose}
              className="absolute top-2 right-2 text-gray-600 hover:text-gray-900"
            >
              ✖
            </button>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition>
  );
};

LoginModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default LoginModal;
