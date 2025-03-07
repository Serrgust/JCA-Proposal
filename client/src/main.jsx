import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import AuthProvider from "./context/AuthProvider"; // ✅ Import Only the Provider
import App from "./App";
import "./index.css";
import Home from "./pages/Home.jsx";
import Proposals from "./pages/Proposals.jsx";
import Users from "./pages/Users.jsx";
import ErrorPage from "./pages/ErrorPage.jsx";
import NotFound from "./pages/NotFound.jsx";
import ProposalDetail from "./pages/ProposalDetail";
import AddProposal from "./pages/AddProposal";
import ProtectedRoute from "./components/ProtectedRoute";

// Define Routes with Protected Routes
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      { path: "/", element: <Home /> },
      {
        path: "/users",
        element: (
          <ProtectedRoute>
            <Users />
          </ProtectedRoute>
        ),
      },
      {
        path: "/proposals",
        element: (
          <ProtectedRoute>
            <Proposals />
          </ProtectedRoute>
        ),
      },
      {
        path: "/proposals/:id",
        element: (
          <ProtectedRoute>
            <ProposalDetail />
          </ProtectedRoute>
        ),
      },
      {
        path: "/add-proposal",
        element: (
          <ProtectedRoute>
            <AddProposal />
          </ProtectedRoute>
        ),
      },
      { path: "*", element: <NotFound /> },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AuthProvider>
      <RouterProvider router={router} fallbackElement={<h1>Loading...</h1>} />
    </AuthProvider>
  </React.StrictMode>
);
