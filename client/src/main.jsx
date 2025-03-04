import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import "./index.css";
import Home from "./pages/Home.jsx";
import Proposals from "./pages/Proposals.jsx";
import Users from "./pages/Users.jsx";
import ErrorPage from "./pages/ErrorPage.jsx"; // ✅ Import ErrorPage
import NotFound from "./pages/NotFound.jsx";
import ProposalDetail from "./pages/ProposalDetail"; // ✅ Import ProposalDetail

// Define Routes with Loaders
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      { path: "/", element: <Home /> },
      { path: "/users", element: <Users /> }, 
      { path: "/proposals", element: <Proposals /> },
      { path: "/proposals/:id", element: <ProposalDetail /> }, // ✅ Add ProposalDetail route
      { path: "*", element: <NotFound /> }// ✅ Handles unknown routes
    ],
  },
]);


ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider
      router={router}
      fallbackElement={<h1>Loading...</h1>} // ✅ Add HydrateFallback
    />
  </React.StrictMode>
);
