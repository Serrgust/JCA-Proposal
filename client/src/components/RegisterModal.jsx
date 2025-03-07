import { useState } from "react";
import PropTypes from "prop-types";
import { API_BASE_URL } from "../config";
import { Dialog, Transition } from "@headlessui/react";
import { Fragment } from "react";

const RegisterModal = ({ isOpen, onClose, isAdmin }) => {
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("user"); // ✅ Default role
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const validateEmail = (email) => email.endsWith("@jcautomation.net");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!validateEmail(email)) {
      setError("Email must be a '@jcautomation.net' address.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          first_name: firstName,
          last_name: lastName,
          email,
          password,
          role,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccessMessage("User registered successfully!");
        setTimeout(() => {
          onClose();
        }, 2000);
      } else {
        setError(data.error || "Registration failed.");
      }
    } catch (err) {
      console.error(err);
      setError("An error occurred during registration.");
    }
  };

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-50" />
        </Transition.Child>

        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0 scale-95"
            enterTo="opacity-100 scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 scale-100"
            leaveTo="opacity-0 scale-95"
          >
            <Dialog.Panel className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full relative">
              {/* Close Button */}
              <button
                onClick={onClose}
                className="absolute top-2 right-2 text-gray-600 hover:text-gray-900"
              >
                ✖
              </button>

              <Dialog.Title className="text-2xl font-semibold text-center mb-4 text-gray-900">
                {isAdmin ? "Create User" : "Register"}
              </Dialog.Title>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-gray-700 font-medium">Username</label>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    className="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 text-gray-900"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-gray-700 font-medium">First Name</label>
                    <input
                      type="text"
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                      required
                      className="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 text-gray-900"
                    />
                  </div>

                  <div>
                    <label className="block text-gray-700 font-medium">Last Name</label>
                    <input
                      type="text"
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)}
                      required
                      className="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 text-gray-900"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-gray-700 font-medium">Email</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 text-gray-900"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-gray-700 font-medium">Password</label>
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      className="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 text-gray-900"
                    />
                  </div>

                  <div>
                    <label className="block text-gray-700 font-medium">Confirm Password</label>
                    <input
                      type="password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                      className="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 text-gray-900"
                    />
                  </div>
                </div>

                {/* ✅ Show Role Selection Only for Admins */}
                {isAdmin && (
                  <div>
                    <label className="block text-gray-700 font-medium">Role</label>
                    <select
                      value={role}
                      onChange={(e) => setRole(e.target.value)}
                      className="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 text-gray-900"
                    >
                      <option value="user">User</option>
                      <option value="moderator">Moderator</option>
                      <option value="admin">Admin</option>
                    </select>
                  </div>
                )}

                <button
                  type="submit"
                  className="w-full bg-green-500 text-white p-3 rounded hover:bg-green-600 transition"
                >
                  {isAdmin ? "Create User" : "Register"}
                </button>
              </form>

              {error && <p className="text-red-500 text-sm mt-2 text-center">{error}</p>}
              {successMessage && <p className="text-green-500 text-sm mt-2 text-center">{successMessage}</p>}
            </Dialog.Panel>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition>
  );
};

RegisterModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  isAdmin: PropTypes.bool.isRequired,
};

export default RegisterModal;
